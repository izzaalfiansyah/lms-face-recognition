import os
from fastapi import UploadFile
from pydantic import BaseModel
import face_recognition

from src.service.face_service.get_user_face_dir import user_face_dir


class StoreFaceParam(BaseModel):
    user_id: int


def store_face(param: StoreFaceParam, images: list[UploadFile]):
    encoded_images = []
    is_path_exists = os.path.exists(user_face_dir(param.user_id))

    if not is_path_exists:
        os.makedirs(user_face_dir(param.user_id))

    for image in images:
        image = face_recognition.load_image_file(image.file)
        encoded_image = face_recognition.face_encodings(image)[0]

        encoded_images.append(encoded_image)

    return {
        "user_id": param.user_id,
        "encoded_images": images,
    }
