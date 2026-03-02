from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_SECRET = os.getenv("API_SECRET")

@app.get("/")
def home():
    return {"status": "API działa"}

@app.get("/inventory/{user_id}")
def inventory(user_id: int, x_api_key: str = ""):
    if x_api_key != API_SECRET:
        return {"error": "Unauthorized"}

    return {
        "userId": user_id,
        "items": [
            {"type": "Gamepass", "name": "VIP", "price": 100}
        ]
    }