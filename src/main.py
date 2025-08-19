import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Oneklik Face Detection")


@app.get("/")
async def root():
    return {
        "message": "Its Work",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=4000, reload=True)
