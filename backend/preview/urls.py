from django.urls import path
from .api.views import (
    BatchIngestAPIView,
    BatchProcessAPIView,
    BatchStatusAPIView,
    PreviewAPIView,
)

urlpatterns = [
    path("", PreviewAPIView.as_view(), name="preview_endpoint"),
    path("batch/", BatchIngestAPIView.as_view(), name="preview_batch_endpoint"),
    path("ingest/", BatchIngestAPIView.as_view(), name="ingest_endpoint"),
    path("<int:batch_id>/status/", BatchStatusAPIView.as_view(), name="batch_status_endpoint"),
    path("<int:batch_id>/process/", BatchProcessAPIView.as_view(), name="process_batch_endpoint"),
]