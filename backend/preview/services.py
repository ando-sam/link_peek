import logging

from django.db import transaction
from django.utils import timezone

from .models import URLBatchRequest, UrlPreview
from .scrapers.base import ScrapeError
from .scrapers.router import UnsupportedPlatformError, get_scraper_for_url
from .validators import validate_social_url

logger = logging.getLogger(__name__)

PREVIEW_KEYS = (
    "url",
    "platform",
    "title",
    "description",
    "image",
    "author",
    "author_url",
    "embed_html",
    "video_url",
    "thumbnail_url",
)


class PreviewService:
    def serialize_preview_data(self, data: dict) -> dict:
        return {key: data.get(key) or None for key in PREVIEW_KEYS}

    def serialize_preview_record(self, preview: UrlPreview) -> dict:
        metadata = preview.metadata or {}
        payload = None

        if preview.status == "success":
            payload = self.serialize_preview_data(
                {
                    "url": preview.normalized_url,
                    "platform": preview.platform,
                    **(preview.details or {}),
                }
            )

        error = preview.error_message or metadata.get("error")
        if preview.status == "failed" and not error:
            error = "Unable to fetch preview."

        return {
            "url": preview.raw_url,
            "platform": preview.platform or None,
            "status": preview.status,
            "preview": payload,
            "error": error,
        }

    def batch_summary(self, batch: URLBatchRequest) -> dict:
        previews = list(batch.previews.all())
        return {
            "pending": sum(1 for item in previews if item.status == "pending"),
            "processing": sum(1 for item in previews if item.status == "processing"),
            "success": sum(1 for item in previews if item.status == "success"),
            "failed": sum(1 for item in previews if item.status == "failed"),
        }

    def normalize_url_list(self, raw_urls):
        valid_urls = []
        validation_errors = []

        for index, url in enumerate(raw_urls):
            if not isinstance(url, str):
                validation_errors.append(
                    {
                        "index": index,
                        "url": str(url),
                        "error": "URL must be a string.",
                    }
                )
                continue

            candidate = url.strip()
            if not candidate:
                validation_errors.append(
                    {
                        "index": index,
                        "url": candidate,
                        "error": "URL cannot be empty.",
                    }
                )
                continue

            try:
                valid_urls.append(validate_social_url(candidate))
            except ValueError as exc:
                validation_errors.append(
                    {
                        "index": index,
                        "url": candidate,
                        "error": str(exc),
                    }
                )

        return valid_urls, validation_errors

    def build_preview_from_scraper(self, raw_url: str) -> dict:
        normalized_url = validate_social_url(raw_url)
        scraper = get_scraper_for_url(normalized_url)
        return self.serialize_preview_data(scraper.fetch_preview())

    def ingest_batch(self, raw_urls):
        cleaned_urls, validation_errors = self.normalize_url_list(raw_urls)
        if not cleaned_urls:
            return None, validation_errors

        with transaction.atomic():
            batch = URLBatchRequest.objects.create(
                urls=cleaned_urls,
                validation_errors=validation_errors,
            )
            preview_records = [
                UrlPreview(
                    batch=batch,
                    raw_url=url,
                    normalized_url=url,
                    platform="",
                    status="pending",
                    description=None,
                    details={},
                    metadata={},
                )
                for url in cleaned_urls
            ]
            UrlPreview.objects.bulk_create(preview_records)

        return batch, validation_errors

    def get_batch_status(self, batch_id: int):
        batch = URLBatchRequest.objects.prefetch_related("previews").get(id=batch_id)
        previews = list(batch.previews.all().order_by("created_at"))
        return batch, previews

    def process_batch(self, batch: URLBatchRequest):
        previews = list(batch.previews.all().order_by("created_at"))
        if not previews:
            previews = [
                UrlPreview(
                    batch=batch,
                    raw_url=url,
                    normalized_url=url,
                    platform="",
                    status="pending",
                    description=None,
                    details={},
                    metadata={},
                )
                for url in batch.urls
            ]
            UrlPreview.objects.bulk_create(previews)

        processed_count = 0
        error_count = 0

        for preview in previews:
            self.process_preview(preview)
            if preview.status == "success":
                processed_count += 1
            else:
                error_count += 1

        return {
            "batch_id": batch.id,
            "processed": processed_count,
            "errors": error_count,
            "total": len(previews),
        }

    def process_preview(self, preview: UrlPreview) -> UrlPreview:
        preview.status = "processing"
        preview.error_message = None
        preview.save(update_fields=["status", "error_message"])

        try:
            preview_data = self.build_preview_from_scraper(preview.raw_url)
            preview.normalized_url = preview_data["url"] or preview.normalized_url
            preview.platform = preview_data["platform"] or preview.platform
            preview.description = preview_data["description"]
            preview.details = {
                key: value
                for key, value in preview_data.items()
                if key in PREVIEW_KEYS and value is not None
            }
            preview.metadata = {}
            preview.status = "success"
        except (ValueError, UnsupportedPlatformError) as exc:
            preview.metadata = {"error": str(exc)}
            preview.error_message = str(exc)
            preview.status = "failed"
        except ScrapeError as exc:
            preview.metadata = {"error": exc.message}
            if exc.status_code is not None:
                preview.metadata["status_code"] = exc.status_code
            preview.error_message = exc.message
            preview.status = "failed"
        except Exception:
            logger.exception("Unexpected error processing %s", preview.raw_url)
            preview.metadata = {"error": "Internal processing error."}
            preview.error_message = "Internal processing error."
            preview.status = "failed"
        finally:
            preview.processed_at = timezone.now()
            preview.save()

        return preview
