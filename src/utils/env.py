import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

app_env = os.getenv("APP_ENV") or "development"

api_lms_url = os.getenv("API_LMS_URL") or "http://localhost:8000/api/development"
api_lms_key = os.getenv("API_LMS_KEY") or "1234"

model_name = os.getenv("MODEL_NAME") or "Facenet"
backend_detector = os.getenv("BACKEND_DETECTOR") or "fastmtcnn"


def is_development():
    return app_env == "development"
