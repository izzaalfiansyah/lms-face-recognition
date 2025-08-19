from fastapi import FastAPI
from src.router import face_router

app = FastAPI(title="Oneklik Face Detection")

app.include_router(face_router.router, prefix="/face")


@app.get("/")
async def root():
    return {
        "message": "Its Work",
    }
