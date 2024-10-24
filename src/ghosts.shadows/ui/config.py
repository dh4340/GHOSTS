import os

# URLs for authentication and shadows services, defaulting to local if environment variables are not set
AUTH_URL = os.getenv("AUTH_URL", "http://127.0.0.1:8000")
SHADOWS_URL = os.getenv("SHADOWS_URL", "http://127.0.0.1:5900")
