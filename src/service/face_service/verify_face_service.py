import os

from deepface import DeepFace
from fastapi import HTTPException
import numpy
from pydantic import BaseModel

from src.service.face_service.get_user_face_dir_service import user_face_dir
from src.utils.env import model_name


class VerifyFaceResult(BaseModel):
    verified: bool
    distance: float
    confidence: float


async def verify_face(user_id: int, image: str) -> VerifyFaceResult:
    user_folder = user_face_dir(user_id)
    print(user_folder)

    if not os.path.exists(user_folder):
        raise HTTPException(404, detail="Face recognition not found")
    #
    # for file in os.scandir(user_folder):
    #     encoded_vector = numpy.load(file.path)
    #     encoded_images.append(encoded_vector)

    results = DeepFace.find(
        img_path=image, db_path="assets/faces/1", model_name=model_name
    )
    # unknown = face_recognition.load_image_file(image)
    # unknown_encoding = face_recognition.face_encodings(unknown)[0]
    #
    # distances = face_recognition.face_distance(encoded_images, unknown_encoding)

    if len(results) == 0:
        raise HTTPException(401, detail="Face recognition not found")

    result = results[0]

    distance = result["distance"].mean()
    confidence = result["confidence"].mean()
    verified = distance < 0.5

    return VerifyFaceResult(verified=verified, distance=distance, confidence=confidence)
