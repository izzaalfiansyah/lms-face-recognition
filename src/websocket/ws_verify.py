from datetime import date
import os
from fastapi import WebSocket
import base64

from src.service.face_service.verify_face_service import verify_face


async def ws_verify_action(ws: WebSocket, user_id, data):
    try:
        if "image" in data:
            base64_image = str(data).split(";base64,")[1]
            decoded_image = base64.b64decode(base64_image)
            filename = "assets/" + date.today().strftime("%d-%m-%Y") + ".jpg"

            with open(filename, "wb") as file:
                file.write(decoded_image)

            result = await verify_face(user_id=user_id, image=filename)

            if result.verified:
                await ws.send_json(
                    {
                        "success": True,
                        "status": "success",
                        "message": "user face recognized",
                        "data": result.model_dump(),
                    }
                )
            else:
                await ws.send_json(
                    {
                        "status": "not_recognized",
                        "message": "user face not recognized",
                        "data": result.model_dump(),
                    }
                )

            os.remove(filename)
        else:
            raise Exception("image not valid")
    except:
        await ws.send_json({"status": "error", "message": "image not valid"})
