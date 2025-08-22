import os
import face_recognition
from fastapi import HTTPException
import numpy
from pydantic import BaseModel

from src.service.face_service.get_user_face_dir_service import user_face_dir


class VerifyFaceResult(BaseModel):
    verified: bool
    distance: float


async def verify_face(user_id: int, image) -> VerifyFaceResult:
    user_folder = user_face_dir(user_id)
    encoded_images = []

    if not os.path.exists(user_folder):
        raise HTTPException(404, detail="Face recognition not found")

    for file in os.scandir(user_folder):
        encoded_vector = numpy.load(file.path)
        encoded_images.append(encoded_vector)

    unknown = face_recognition.load_image_file(image)
    unknown_encoding = face_recognition.face_encodings(unknown)[0]

    distances = face_recognition.face_distance(encoded_images, unknown_encoding)

    distance = numpy.array(distances).mean()
    verified = distance < 0.5

    return VerifyFaceResult(verified=verified, distance=distance)
