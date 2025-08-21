# interview/views.py
import os, tempfile, time, json
from django.utils import timezone
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .serializers import StartInterviewRequestSerializer
from .models import InterviewSession, InterviewResponse

MODE = os.getenv("MONICA_AI_MODE", "REMOTE")

if MODE.upper() == "REMOTE":
    from .services.ai_client import (
        start_session as ai_start,
        get_current_question as ai_current,
        speak_question as ai_speak,
        submit_audio as ai_submit,
        get_report as ai_report,
    )
else:
    from .services.local_ai import (
        start_session_local as ai_start,
        # ... implement local funcs with same signatures
    )

@api_view(["POST"])
def start_interview(request):
    ser = StartInterviewRequestSerializer(data=request.data)
    if not ser.is_valid():
        return HttpResponseBadRequest(json.dumps(ser.errors), content_type="application/json")
    data = ser.validated_data

    # call AI service
    ai = ai_start(data["candidate_name"], data["position"], data.get("custom_questions"))

    # persist session
    sess = InterviewSession.objects.create(
        id=ai["session_id"],
        candidate_name=data["candidate_name"],
        position=data["position"],
        status="not_started",
        current_index=0,
    )
    return JsonResponse({
        "session_id": ai["session_id"],
        "message": f"Session created for {data['candidate_name']}",
        "first_question": ai.get("first_question"),
        "total_questions": ai.get("total_questions", 0),
    })

@api_view(["GET"])
def get_status(request, session_id: str):
    try:
        sess = InterviewSession.objects.get(id=session_id)
    except InterviewSession.DoesNotExist:
        return HttpResponseBadRequest("Session not found")
    total = 8  # if needed, you can fetch from AI or store
    return JsonResponse({
        "session_id": str(sess.id),
        "status": sess.status,
        "current_question": sess.current_index + 1,
        "total_questions": total,
        "progress_pct": (sess.current_index / max(total,1)) * 100,
    })

@api_view(["GET"])
def current_question(request, session_id: str):
    ai = ai_current(session_id)
    return JsonResponse(ai)

@api_view(["POST"])
def speak_question(request, session_id: str):
    ai = ai_speak(session_id)
    return JsonResponse(ai)

@csrf_exempt
@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def submit_response(request):
    session_id = request.POST.get("session_id")
    if not session_id:
        return HttpResponseBadRequest("session_id is required")

    f = request.FILES.get("audio")
    if not f:
        return HttpResponseBadRequest("audio file is required")

    # Save a temp wav
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        for chunk in f.chunks():
            tmp.write(chunk)
        tmp_path = tmp.name

    # call AI
    ai = ai_submit(session_id, tmp_path)

    # update session index if needed
    InterviewSession.objects.filter(id=session_id).update(status="in_progress")
    # You can also create InterviewResponse rows here if ai returns details

    # cleanup
    try: os.remove(tmp_path)
    except: pass

    return JsonResponse(ai)

@api_view(["GET"])
def get_report(request, session_id: str):
    ai = ai_report(session_id)
    # optionally mark complete
    # InterviewSession.objects.filter(id=session_id).update(status="completed", completed_at=timezone.now())
    return JsonResponse(ai)
