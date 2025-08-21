# monica_backend/settings.py

INSTALLED_APPS = [
    # ...
    "corsheaders",
    "rest_framework",
    "interview",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    # ...
]

CORS_ALLOW_ALL_ORIGINS = True  # prod me restrict karna
# ya CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]

# DRF basic config (optional)
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
}

# ENV based toggle: AI ko HTTP microservice se call karein
import os
MONICA_AI_MODE = os.getenv("MONICA_AI_MODE", "REMOTE")  # "REMOTE" | "LOCAL"
MONICA_AI_BASE_URL = os.getenv("MONICA_AI_BASE_URL", "http://localhost:8000")

# Debugging
DEBUG = True   # Dev ke liye True rakho

# Hosts allowed (development ke liye sab allow)
ALLOWED_HOSTS = ["*"]

# Agar production ke liye chahiye to yeh use karna:
# DEBUG = False
# ALLOWED_HOSTS = ["yourdomain.com", "127.0.0.1", "localhost"]
ROOT_URLCONF = "monica_backend.urls"
