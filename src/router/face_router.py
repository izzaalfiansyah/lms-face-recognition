import base64
from datetime import date
import os
import uuid
from fastapi import APIRouter, Form, HTTPException, UploadFile
from src.service.face_service.store_face_service import StoreFaceParam, store_face
from src.service.face_service.verify_face_service import verify_face
from src.utils.temp_dir import get_temp_dir

router = APIRouter()


@router.post("/")
async def store(user_id: int = Form(), images: list[UploadFile] = []):
    if len(images) == 0:
        raise HTTPException(status_code=422, detail="Images not found")

    result = store_face(StoreFaceParam(user_id=user_id), images)

    return {
        "message": f"{result.success} images successfully saved",
    }


@router.post("/verify")
async def verify(
    user_id: int = Form(),
    image: UploadFile | None = None,
    image_base64: str | None = Form(default=""),
):
    img_path = ""

    if image is None and image_base64 is None:
        raise HTTPException(status_code=422, detail="Image not found")

    filename = get_temp_dir() + uuid.uuid4().hex + ".jpg"

    if image_base64 is not None and image_base64 != "":
        with open(filename, "wb") as file:
            base64_image = str(image_base64).split(";base64,")[1]
            decoded_image = base64.b64decode(base64_image)

            file.write(decoded_image)
            img_path = filename

    if image is not None:
        with open(filename, "wb") as file:
            file.write(image.file.read())
            img_path = filename

    try:
        result = await verify_face(user_id, img_path)
        os.remove(img_path)

        if not result.verified:
            raise HTTPException(401, "User face not recognized")

        return {
            "success": result.verified,
            "message": "User face recognized",
            "data": result.model_dump(),
        }
    except Exception as e:
        os.remove(img_path)
        raise HTTPException(401, "User face not recognized")
