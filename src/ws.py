from fastapi import WebSocket
from src.websocket.ws_verify import ws_verify_action


async def runWs(ws: WebSocket):
    await ws.accept()

    while True:
        try:
            messageJson = await ws.receive_json()

            type = messageJson["type"]
            data = messageJson["data"]
            user_id = messageJson["user_id"]

            if not user_id:
                await ws.send_json({"message": "user not found"})
                continue

            if type == "verify":
                await ws_verify_action(ws, user_id, data)
        except Exception as _:
            await ws.send_json({"message": "data not completed"})
