# interview/services/local_ai.py
# NOTE: Only if you install torch/librosa/whisper etc. locally.
def start_session_local(candidate_name, position, custom_questions=None):
    # TODO: implement using your earlier Monica classes
    return {"session_id":"local_123","total_questions":8,"first_question":"Tell me about yourself."}

# ...and same shape funcs as ai_client.py
