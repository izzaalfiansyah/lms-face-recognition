from fastapi import FastAPI, WebSocket
from src import ws
from src.router import face_router

app = FastAPI(title="Oneklik Face Detection")

app.include_router(face_router.router, prefix="/face")


@app.get("/")
async def root():
    return {
        "message": "Its Work",
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws.runWs(websocket)
