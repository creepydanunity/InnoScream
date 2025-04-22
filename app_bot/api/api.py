import os
from dotenv import load_dotenv
import httpx


API_URL = os.getenv("API_URL")


async def post_scream(content: str, user_id: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_URL}/scream", json={"content": content, "user_id": user_id})
        return resp.json()
    
async def delete_scream(scream_id: int, user_id: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_URL}/delete", json={"scream_id": scream_id, "user_id": user_id})
        resp.raise_for_status()
        return resp.json()

async def react_to_scream(scream_id: int, emoji: str, user_id: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_URL}/react", json={
            "scream_id": scream_id,
            "emoji": emoji,
            "user_id": user_id
        })
        return resp.json()

async def get_next_scream(user_id: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_URL}/feed/{user_id}")
        resp.raise_for_status()
        return resp.json()
    
async def get_all_screams_for_admin():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_URL}/screams/admin")
        resp.raise_for_status()
        return resp.json()

async def get_user_stats(user_id: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_URL}/stats/{user_id}")
        return resp.json()

async def get_stress_stats():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_URL}/stats/weekly")
        return resp.json()
