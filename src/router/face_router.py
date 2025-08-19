from fastapi import APIRouter, Form, UploadFile
from src.service.face_service.store_face import StoreFaceParam, store_face
from src.service.face_service.verify_face_service import verify_face

router = APIRouter()


@router.post("/")
async def store(user_id: int = Form(), file: list[UploadFile] = []):
    result = store_face(StoreFaceParam(user_id=user_id), file)
    return result


@router.post("/verify")
async def detect():
    verify_face("src/assets/turis.webp")
    return {"message": "Something wrong"}
