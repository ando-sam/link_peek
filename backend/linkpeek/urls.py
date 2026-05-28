from django.urls import include, path

from preview.api.views import BatchIngestAPIView

urlpatterns = [
    path("api/ingest/", BatchIngestAPIView.as_view(), name="ingest_endpoint_root"),
    path("api/preview/", include("preview.urls")),
]
