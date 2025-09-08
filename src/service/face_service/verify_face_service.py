import os

from deepface import DeepFace
from fastapi import HTTPException
from pydantic import BaseModel
import requests

from src.service.face_service.get_user_face_dir_service import user_face_dir
from src.utils.env import model_name, backend_detector, api_lms_url, api_lms_key


class VerifyFaceResult(BaseModel):
    verified: bool
    distance: float
    confidence: float


def parse_result(distance: float, confidence: float) -> VerifyFaceResult:
    verified = distance < 0.5

    return VerifyFaceResult(verified=verified, distance=distance, confidence=confidence)


async def verify_face(user_id: int, img_path: str) -> VerifyFaceResult:
    user_folder = user_face_dir(user_id)

    profile_path = (
        api_lms_url + "/users/" + str(user_id) + "/profile?test_auth_id=" + str(user_id)
    )

    try:
        res = requests.get(
            profile_path,
            headers={
                "x-api-key": api_lms_key,
            },
        )

        if res.status_code != 200:
            raise HTTPException(404, detail="User not found")

        data = res.json()

        if data["success"] is not True:
            raise HTTPException(404, detail="User not found")

        avatar = data["data"]["user"]["avatar"]

        if avatar is None:
            raise HTTPException(404, detail="User avatar not found")

        avatar_res = requests.get(avatar)
        filename = "assets/temp/" + str(user_id) + ".jpg"

        if avatar_res.status_code != 200:
            os.remove(filename)
            raise HTTPException(404, detail="User avatar not found")

        with open(filename, "wb") as file:
            file.write(avatar_res.content)

        result = DeepFace.verify(
            img1_path=img_path,
            img2_path=filename,
            model_name=model_name,
            detector_backend=backend_detector,
        )

        os.remove(filename)

        return parse_result(result["distance"], result["confidence"])
    except Exception as err:
        print(err)

    if not os.path.exists(user_folder):
        raise HTTPException(404, detail="Resource face not found")

    results = DeepFace.find(
        img_path=img_path,
        db_path=user_folder,
        model_name=model_name,
        detector_backend=backend_detector,
    )

    if len(results) == 0:
        raise HTTPException(401, detail="Face recognition not found")

    result = results[0]

    distance: float = result["distance"].mean()
    confidence: float = result["confidence"].mean()

    return parse_result(distance=distance, confidence=confidence)
