# interview/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("interview/start", views.start_interview),
    path("interview/status/<str:session_id>", views.get_status),
    path("interview/current-question/<str:session_id>", views.current_question),
    path("interview/speak/<str:session_id>", views.speak_question),  # optional
    path("interview/submit", views.submit_response),  # multipart audio upload
    path("interview/report/<str:session_id>", views.get_report),
]
