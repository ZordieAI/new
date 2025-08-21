# interview/models.py
from django.db import models
from django.utils import timezone
import uuid

class InterviewSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    candidate_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    status = models.CharField(max_length=30, default="not_started")  # not_started | in_progress | completed
    current_index = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)

class InterviewResponse(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name="responses")
    question_id = models.CharField(max_length=50)
    question_text = models.TextField()
    transcript = models.TextField()
    audio_duration = models.FloatField(default=0)
    transcript_confidence = models.FloatField(default=0)
    emotional_json = models.JSONField(default=dict)
    flags_json = models.JSONField(default=list)
    created_at = models.DateTimeField(default=timezone.now)
