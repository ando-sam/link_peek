from django.urls import path
from .views import preview_endpoint

urlpatterns = [
    path("", preview_endpoint, name="preview_endpoint"),
]
