from django.core.exceptions import ValidationError
from django.db import models


PREVIEW_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("processing", "Processing"),
    ("success", "Success"),
    ("failed", "Failed"),
]


class URLBatchRequest(models.Model):
    urls = models.JSONField(help_text="List of social URLs to preview")
    validation_errors = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not isinstance(self.urls, list):
            raise ValidationError({"urls": "Expected a list of URLs."})
        if not self.urls:
            raise ValidationError({"urls": "At least one URL is required."})
        if any(not isinstance(url, str) or not url.strip() for url in self.urls):
            raise ValidationError({"urls": "All URLs must be non-empty strings."})

    def __str__(self):
        return f"URLBatchRequest(id={self.id}, count={len(self.urls)})"


class UrlPreview(models.Model):
    batch = models.ForeignKey(
        URLBatchRequest,
        related_name="previews",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    raw_url = models.URLField()
    normalized_url = models.URLField()
    platform = models.CharField(max_length=32, blank=True, default="")
    status = models.CharField(max_length=16, choices=PREVIEW_STATUS_CHOICES, default="pending")
    description = models.TextField(null=True, blank=True)
    details = models.JSONField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "URL Preview"
        verbose_name_plural = "URL Previews"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.raw_url} ({self.status})"
