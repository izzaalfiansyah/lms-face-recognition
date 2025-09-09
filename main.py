import uvicorn
from dotenv import load_dotenv

from src.utils import env

load_dotenv()

print(f"Avatar source: {env.api_lms_url}")

if __name__ == "__main__":
    uvicorn.run("src.app:app", host="0.0.0.0", port=4000, reload=env.is_development())
