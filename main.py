import httpx
from fastapi import FastAPI, Header
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

@app.get("/inventory/{user_id}")
async def inventory(user_id: int, x_api_key: str = Header(default="")):
    if x_api_key != API_SECRET:
        return {"error": "Unauthorized"}

    async with httpx.AsyncClient() as client:
        games_resp = await client.get(
            f"https://games.roblox.com/v2/users/{user_id}/games",
            params={"accessFilter": "All", "limit": 50}
        )
        games_data = games_resp.json().get("data", [])

        all_gamepasses = []

        for game in games_data:
            gp_resp = await client.get(
                f"https://games.roblox.com/v1/games/{game['id']}/game-passes",
                params={"limit": 100}
            )
            passes = gp_resp.json().get("data", [])
            for p in passes:
                all_gamepasses.append({
                    "type": "Gamepass",
                    "gameName": game["name"],
                    "passName": p["name"],
                    "price": p.get("price", 0)
                })

        clothing_resp = await client.get(
            "https://catalog.roblox.com/v1/search/items",
            params={
                "category": "Clothing",
                "creatorTargetId": user_id,
                "creatorType": "User",
                "limit": 100
            }
        )
        clothing_data = clothing_resp.json().get("data", [])

        clothing_items = [
            {
                "type": "Clothing",
                "name": item["name"],
                "assetType": item["assetType"],
                "price": item.get("price", 0)
            }
            for item in clothing_data
        ]

        # ----------------------------
        # 3️⃣ Połącz wszystko w jedną listę
        # ----------------------------
        return {"items": all_gamepasses + clothing_items}
