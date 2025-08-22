from fastapi import APIRouter, Form, HTTPException, UploadFile
from src.service.face_service.store_face_service import StoreFaceParam, store_face
from src.service.face_service.verify_face_service import verify_face

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
async def verify(user_id: int = Form(), image: UploadFile | None = None):
    if image is None:
        raise HTTPException(status_code=422, detail="Image not found")

    result = await verify_face(user_id, image.file)

    if not result.verified:
        raise HTTPException(401, "user face not recognized")

    return {
        "success": result.verified,
        "message": "user face recognized",
        "data": result.model_dump(),
    }
