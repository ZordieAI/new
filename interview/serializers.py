# interview/serializers.py
from rest_framework import serializers

class StartInterviewRequestSerializer(serializers.Serializer):
    candidate_name = serializers.CharField()
    position = serializers.CharField()
    custom_questions = serializers.ListField(
        child=serializers.CharField(), required=False, allow_null=True
    )
