import os
from fastapi import UploadFile
from pydantic import BaseModel
import face_recognition
import numpy as np

from src.service.face_service.get_user_face_dir import user_face_dir


class StoreFaceParam(BaseModel):
    user_id: int


def store_face(param: StoreFaceParam, images: list[UploadFile]) -> tuple[int, int, int]:
    is_path_exists = os.path.exists(user_face_dir(param.user_id))
    user_folder = user_face_dir(param.user_id)

    if is_path_exists:
        for file in os.scandir(user_folder):
            os.remove(file.path)
    else:
        os.makedirs(user_folder)

    index = 0
    total = len(images)

    for image in images:
        try:
            image_file = face_recognition.load_image_file(image.file)
            encoded_image = face_recognition.face_encodings(image_file)[0]

            np.save(user_face_dir(param.user_id) + "/" + str(index), encoded_image)
            index += 1
        except:
            pass

    success = index
    failed = total - success
    return (total, success, failed)
