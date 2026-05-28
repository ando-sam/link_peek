from rest_framework import serializers

from ..validators import validate_social_url


class PreviewQuerySerializer(serializers.Serializer):
    url = serializers.CharField(trim_whitespace=True)

    def validate_url(self, value: str) -> str:
        return validate_social_url(value)


class BatchIngestRequestSerializer(serializers.Serializer):
    urls = serializers.ListField(child=serializers.JSONField(), allow_empty=False)


class PreviewDataSerializer(serializers.Serializer):
    url = serializers.CharField(allow_null=True, required=False)
    platform = serializers.CharField(allow_null=True, required=False)
    title = serializers.CharField(allow_null=True, required=False)
    description = serializers.CharField(allow_null=True, required=False)
    image = serializers.CharField(allow_null=True, required=False)
    author = serializers.CharField(allow_null=True, required=False)
    author_url = serializers.CharField(allow_null=True, required=False)
    embed_html = serializers.CharField(allow_null=True, required=False)
    video_url = serializers.CharField(allow_null=True, required=False)
    thumbnail_url = serializers.CharField(allow_null=True, required=False)


class BatchPreviewResultSerializer(serializers.Serializer):
    url = serializers.CharField()
    platform = serializers.CharField(allow_null=True, required=False)
    status = serializers.CharField()
    preview = PreviewDataSerializer(allow_null=True, required=False)
    error = serializers.CharField(allow_null=True, required=False)


class BatchIngestResponseSerializer(serializers.Serializer):
    batch_id = serializers.IntegerField()
    count = serializers.IntegerField()
    status = serializers.CharField()
    errors = serializers.ListField(child=serializers.DictField(), required=False)


class BatchStatusResponseSerializer(serializers.Serializer):
    batch_id = serializers.IntegerField()
    count = serializers.IntegerField()
    urls = serializers.ListField(child=serializers.CharField())
    validation_errors = serializers.ListField(child=serializers.DictField(), required=False)
    summary = serializers.DictField(child=serializers.IntegerField())
    created_at = serializers.DateTimeField()
    results = BatchPreviewResultSerializer(many=True)


class BatchProcessResponseSerializer(serializers.Serializer):
    batch_id = serializers.IntegerField()
    processed = serializers.IntegerField()
    errors = serializers.IntegerField()
    total = serializers.IntegerField()
