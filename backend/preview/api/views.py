from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_202_ACCEPTED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_502_BAD_GATEWAY,
)
from rest_framework.views import APIView

from ..models import URLBatchRequest
from ..scrapers.base import ScrapeError
from ..scrapers.router import UnsupportedPlatformError
from ..services import PreviewService
from .serializers import (
    BatchIngestRequestSerializer,
    BatchIngestResponseSerializer,
    BatchProcessResponseSerializer,
    BatchStatusResponseSerializer,
    PreviewDataSerializer,
    PreviewQuerySerializer,
)


class BasePreviewAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    service = PreviewService()


class PreviewAPIView(BasePreviewAPIView):
    def get(self, request):
        serializer = PreviewQuerySerializer(data=request.query_params)
        if not serializer.is_valid():
            errors = serializer.errors
            if "url" not in errors:
                return Response({"detail": "Missing url query parameter."}, status=HTTP_400_BAD_REQUEST)
            return Response(errors, status=HTTP_400_BAD_REQUEST)

        try:
            preview = self.service.build_preview_from_scraper(serializer.validated_data["url"])
            return Response(PreviewDataSerializer(preview).data, status=HTTP_200_OK)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=HTTP_400_BAD_REQUEST)
        except UnsupportedPlatformError as exc:
            return Response({"detail": str(exc)}, status=HTTP_400_BAD_REQUEST)
        except ScrapeError as exc:
            status_code = exc.status_code or HTTP_502_BAD_GATEWAY
            return Response({"detail": exc.message}, status=status_code)
        except Exception:
            return Response(
                {"detail": "Unable to fetch preview from the target URL."},
                status=HTTP_502_BAD_GATEWAY,
            )


class BatchIngestAPIView(BasePreviewAPIView):
    def post(self, request):
        serializer = BatchIngestRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)

        batch, validation_errors = self.service.ingest_batch(serializer.validated_data["urls"])
        if batch is None:
            return Response(
                {
                    "detail": "No valid URLs provided.",
                    "errors": validation_errors,
                },
                status=HTTP_422_UNPROCESSABLE_ENTITY,
            )

        response = {
            "batch_id": batch.id,
            "count": len(batch.urls),
            "status": "ingested",
        }
        if validation_errors:
            response["errors"] = validation_errors

        return Response(BatchIngestResponseSerializer(response).data, status=HTTP_202_ACCEPTED)


class BatchStatusAPIView(BasePreviewAPIView):
    def get(self, request, batch_id):
        try:
            batch, previews = self.service.get_batch_status(batch_id)
        except URLBatchRequest.DoesNotExist:
            return Response({"detail": "Batch not found."}, status=HTTP_404_NOT_FOUND)

        response = {
            "batch_id": batch.id,
            "count": len(previews),
            "urls": batch.urls,
            "validation_errors": batch.validation_errors or [],
            "summary": self.service.batch_summary(batch),
            "created_at": batch.created_at,
            "results": [self.service.serialize_preview_record(preview) for preview in previews],
        }
        return Response(BatchStatusResponseSerializer(response).data, status=HTTP_200_OK)


class BatchProcessAPIView(BasePreviewAPIView):
    def post(self, request, batch_id):
        try:
            batch = URLBatchRequest.objects.prefetch_related("previews").get(id=batch_id)
        except URLBatchRequest.DoesNotExist:
            return Response({"detail": "Batch not found."}, status=HTTP_404_NOT_FOUND)

        response = self.service.process_batch(batch)
        return Response(BatchProcessResponseSerializer(response).data, status=HTTP_200_OK)
