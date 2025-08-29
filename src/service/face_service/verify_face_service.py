import os

from deepface import DeepFace
from fastapi import HTTPException
from pydantic import BaseModel

from src.service.face_service.get_user_face_dir_service import user_face_dir
from src.utils.env import model_name


class VerifyFaceResult(BaseModel):
    verified: bool
    distance: float
    confidence: float


async def verify_face(user_id: int, img_path: str) -> VerifyFaceResult:
    user_folder = user_face_dir(user_id)

    if not os.path.exists(user_folder):
        raise HTTPException(404, detail="Resource face not found")

    results = DeepFace.find(
        img_path=img_path, db_path=user_folder, model_name=model_name
    )

    if len(results) == 0:
        raise HTTPException(401, detail="Face recognition not found")

    result = results[0]

    distance = result["distance"].mean()
    confidence = result["confidence"].mean()
    verified = distance < 0.5

    return VerifyFaceResult(verified=verified, distance=distance, confidence=confidence)
