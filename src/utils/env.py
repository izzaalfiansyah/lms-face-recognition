import os


model_name = os.getenv("MODEL_NAME") or "Facenet"
backend_detector = os.getenv("BACKEND_DETECTOR") or "fastmtcnn"
