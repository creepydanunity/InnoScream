import os
from dotenv import load_dotenv
import httpx
from app_bot.logger import logger

API_URL = os.getenv("API_URL")

async def post_scream(content: str, user_id: str):
    try:
        logger.debug(f"Posting scream from user {user_id}")
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{API_URL}/scream", json={"content": content, "user_id": user_id})
            logger.info(f"Scream posted successfully, response: {resp.json()}")
            return resp.json()
    except Exception as e:
        logger.error(f"Failed to post scream: {str(e)}", exc_info=True)
        raise

async def create_admin(user_id: str, user_id_to_admin: str):
    try:
        logger.debug(f"Creating admin from {user_id} for {user_id_to_admin}")
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{API_URL}/create_admin", json={"user_id_to_admin": user_id_to_admin, "user_id": user_id})
            resp.raise_for_status()
            logger.info("Admin created successfully")
            return resp.json()
    except Exception as e:
        logger.error(f"Admin creation failed: {str(e)}", exc_info=True)
        raise

async def get_my_id(user_id: str):
    try:
        logger.debug(f"Getting ID for user {user_id}")
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{API_URL}/my_id", json={"user_id": user_id})
            logger.info(f"Received ID response: {resp.json()}")
            return resp.json()
    except Exception as e:
        logger.error(f"Failed to get ID: {str(e)}", exc_info=True)
        raise
    
async def delete_scream(scream_id: int, user_id: str):
    try:
        logger.debug(f"Deleting scream {scream_id} by user {user_id}")
        async with httpx.AsyncClient() as client:
            resp = await client.delete(f"{API_URL}/delete", json={"scream_id": scream_id, "user_id": user_id})
            resp.raise_for_status()
            logger.info("Scream deleted successfully")
            return resp.json()
    except Exception as e:
        logger.error(f"Scream deletion failed: {str(e)}", exc_info=True)
        raise
    
async def confirm_scream(scream_id: int, user_id: str):
    try:
        logger.debug(f"Confirming scream {scream_id} by user {user_id}")
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{API_URL}/confirm", json={"scream_id": scream_id, "user_id": user_id})
            resp.raise_for_status()
            logger.info("Scream confirmed successfully")
            return resp.json()
    except Exception as e:
        logger.error(f"Scream confirmation failed: {str(e)}", exc_info=True)
        raise

async def react_to_scream(scream_id: int, emoji: str, user_id: str):
    try:
        logger.debug(f"Reacting to scream {scream_id} with {emoji} by user {user_id}")
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{API_URL}/react", json={
                "scream_id": scream_id,
                "emoji": emoji,
                "user_id": user_id
            })
            logger.info(f"Reaction recorded: {resp.json()}")
            return resp.json()
    except Exception as e:
        logger.error(f"Reaction failed: {str(e)}", exc_info=True)
        raise

async def get_next_scream(user_id: str):
    try:
        logger.debug(f"Getting next scream for user {user_id}")
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{API_URL}/feed/{user_id}")
            resp.raise_for_status()
            logger.info("Scream retrieved successfully")
            return resp.json()
    except Exception as e:
        logger.error(f"Failed to get scream: {str(e)}", exc_info=True)
        raise
    
async def get_all_screams_for_admin(user_id: str):
    try:
        logger.debug(f"Getting all screams for admin {user_id}")
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{API_URL}/screams/admin", json={
                "user_id": user_id
            })
            resp.raise_for_status()
            logger.info("Admin screams retrieved successfully")
            return resp.json()
    except Exception as e:
        logger.error(f"Failed to get admin screams: {str(e)}", exc_info=True)
        raise

async def get_user_stats(user_id: str):
    try:
        logger.debug(f"Getting stats for user {user_id}")
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{API_URL}/stats/{user_id}")
            resp.raise_for_status()
            logger.info("User stats retrieved successfully")
            return resp.json()
    except Exception as e:
        logger.error(f"Failed to get user stats: {str(e)}", exc_info=True)
        raise

async def get_stress_stats():
    try:
        logger.debug("Getting weekly stress stats")
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{API_URL}/stats/weekly")
            logger.info("Stress stats retrieved successfully")
            return resp.json()
    except Exception as e:
        logger.error(f"Failed to get stress stats: {str(e)}", exc_info=True)
        raise

async def get_top_screams(n: int = 3):
    try:
        logger.debug(f"Getting top {n} screams")
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{API_URL}/top")
            logger.info("Top screams retrieved successfully")
            return resp.json()
    except Exception as e:
        logger.error(f"Failed to get top screams: {str(e)}", exc_info=True)
        raise

async def get_history():
    try:
        logger.debug("Fetching available historical weeks")
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{API_URL}/history")
            resp.raise_for_status()
            data = resp.json()
            return data.get("weeks", [])
    except Exception as e:
        logger.error(f"Failed to get history: {str(e)}", exc_info=True)
        raise

async def get_historical_week(week_id: str):
    try:
        logger.debug(f"Fetching historical week {week_id}")
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{API_URL}/history/{week_id}")
            resp.raise_for_status()
            data = resp.json()
            
            top_three = data.get("posts", [])[:3]
            logger.info(f"Retrieved {len(top_three)} screams for week {week_id}")
            return top_three
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            logger.warning(f"Week {week_id} not found")
            raise ValueError("Week not found in archive")
        raise
    except Exception as e:
        logger.error(f"Failed to get historical week: {str(e)}", exc_info=True)
        raise

async def archive_current_week(week_id: str, user_id: str):
    try:
        logger.debug(f"Archiving week as {week_id}")
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{API_URL}/history/{week_id}",
                json={"user_id": user_id}
            )
            resp.raise_for_status()
            logger.info(f"Week {week_id} archived successfully")
            return resp.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 409:
            logger.warning(f"Week {week_id} already exists")
            raise ValueError("Week already archived") from e
        raise
    except Exception as e:
        logger.error(f"Failed to archive week: {str(e)}", exc_info=True)
        raise

