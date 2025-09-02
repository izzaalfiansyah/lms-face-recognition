import os
from typing import Any, Dict
from fastapi import UploadFile
from pydantic import BaseModel
from deepface import DeepFace
import numpy as np

from src.service.face_service.get_user_face_dir_service import user_face_dir
from src.utils.env import model_name, backend_detector


class StoreFaceParam(BaseModel):
    user_id: int


class StoreFaceResult(BaseModel):
    total: int
    success: int
    failed: int


def store_face(param: StoreFaceParam, images: list[UploadFile]) -> StoreFaceResult:
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
            image.file.seek(0)
            extension = str(image.filename).split(".")[-1]
            filename = user_face_dir(param.user_id) + "/" + str(index) + "." + extension

            with open(filename, "wb") as file:
                file.write(image.file.read())

            embeddings = DeepFace.represent(
                img_path=filename,
                model_name=model_name,
                detector_backend=backend_detector,
            )

            index += 1
        except Exception as err:
            print(err)
            pass

    success = index
    failed = total - success
    return StoreFaceResult(total=total, success=success, failed=failed)
