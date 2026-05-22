from django.urls import include, path

urlpatterns = [
    path("api/preview/", include("preview.urls")),
]
