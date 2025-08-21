# interview/services/ai_client.py
import os
import requests

BASE_URL = os.getenv("MONICA_AI_BASE_URL", "http://localhost:8000")

def start_session(candidate_name: str, position: str, custom_questions=None):
    payload = {
        "candidate_name": candidate_name,
        "position": position,
        "custom_questions": custom_questions or [],
    }
    r = requests.post(f"{BASE_URL}/api/interview/start", json=payload, timeout=60)
    r.raise_for_status()
    return r.json()

def get_current_question(session_id: str):
    r = requests.get(f"{BASE_URL}/api/interview/{session_id}/current-question", timeout=60)
    r.raise_for_status()
    return r.json()

def speak_question(session_id: str):
    r = requests.post(f"{BASE_URL}/api/interview/{session_id}/speak-question", timeout=120)
    r.raise_for_status()
    return r.json()

def submit_audio(session_id: str, file_path: str):
    with open(file_path, "rb") as f:
        files = {"audio_file": ("input.wav", f, "audio/wav")}
        r = requests.post(
            f"{BASE_URL}/api/interview/{session_id}/submit-response",
            files=files,
            timeout=600,
        )
    r.raise_for_status()
    return r.json()

def get_report(session_id: str):
    r = requests.get(f"{BASE_URL}/api/interview/{session_id}/report", timeout=120)
    r.raise_for_status()
    return r.json()
