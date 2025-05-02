import os
from dotenv import load_dotenv
import httpx
from app_bot.logger import logger

API_URL = os.getenv("API_URL")

async def post_scream(content: str, user_id: str):
    """
    Submit a new scream to the backend.

    Args:
        content (str): The textual content of the scream.
        user_id (str): The ID of the user posting the scream.

    Returns:
        dict: Response JSON containing the scream ID and status.

    Raises:
        Exception: On request failure or server error.
    """

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

    """
    Creates an admin user by sending a POST request to the API.

    Args:
        user_id (str): The user ID making the request.
        user_id_to_admin (str): The user ID to be granted admin privileges.

    Returns:
        dict: The response JSON from the API indicating the success or failure of the operation.

    Raises:
        httpx.HTTPStatusError: If the API responds with a non-2xx status code.
    """

    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_URL}/create_admin", json={"user_id_to_admin": user_id_to_admin, "user_id": user_id})
        resp.raise_for_status()
        return resp.json()
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

    """
    Retrieves the user ID from the API for a given user.

    Args:
        user_id (str): The user ID to query.

    Returns:
        dict: The response JSON from the API containing user ID.
    """

    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_URL}/my_id", json={"user_id": user_id})
        return resp.json()


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

    """
    Deletes a specific scream by its ID by sending a POST request to the API.

    Args:
        scream_id (int): The ID of the scream to be deleted.
        user_id (str): The user ID who is performing the deletion.

    Returns:
        dict: The response JSON from the API confirming the deletion.

    Raises:
        httpx.HTTPStatusError: If the API responds with a non-2xx status code.
    """

    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_URL}/delete", json={"scream_id": scream_id, "user_id": user_id})
        resp.raise_for_status()
        return resp.json()

  
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
    """
    Confirm a scream as reviewed.

    Args:
        scream_id (int): The ID of the scream to confirm.
        user_id (str): The ID of the admin confirming the scream.

    Returns:
        dict: Response JSON indicating success.

    Raises:
        Exception: On failure to complete the request.
    """

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
    """
    Send a reaction to a scream on behalf of a user.

    Args:
        scream_id (int): The ID of the scream to react to.
        emoji (str): The emoji representing the user's reaction.
        user_id (str): The external user ID of the reacting user.

    Returns:
        dict: The JSON response from the backend.

    Behavior:
        - Sends a POST request to the `/react` endpoint with the scream ID, emoji, and user ID.
        - Returns the parsed JSON response from the backend API.
    """
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
    """
    Fetch the next unseen scream for the given user from the backend API.

    Args:
        user_id (str): The external user ID.

    Returns:
        dict: A JSON object containing the next scream's ID and content.

    Raises:
        httpx.HTTPStatusError: If the backend API returns an error.
    """

    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_URL}/feed/{user_id}")
        resp.raise_for_status()
        return resp.json()


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
    """
    Retrieve all unmoderated screams for the admin.

    Args:
        user_id (str): The admin's user ID.

    Returns:
        dict: List of unmoderated screams with content and IDs.

    Raises:
        Exception: On failure to fetch data.
    """

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
    """
    Fetch user scream statistics from the backend API.

    Args:
        user_id (str): The external user ID.

    Returns:
        dict: A JSON object containing the user's scream and reaction statistics.

    Raises:
        httpx.HTTPStatusError: If the backend API responds with an error status.
    """

    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_URL}/stats/{user_id}")
        resp.raise_for_status()
        return resp.json()
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
    """
    Fetch the collective weekly stress statistics from the backend API.

    Returns:
        dict: A JSON object containing the URL to the generated stress chart.

    Raises:
        httpx.HTTPStatusError: If the backend API responds with an error status.
    """

    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_URL}/stress")
        resp.raise_for_status()
        return resp.json()
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
    """
    Fetch the top screams from the backend API.

    Args:
        n (int, optional): The number of top screams to request. Defaults to 3.

    Returns:
        dict: The JSON response from the API containing the top screams.
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_URL}/top")
        return resp.json()
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
    """
    Retrieve the list of archived week identifiers.

    Returns:
        list: A list of strings representing archived weeks.

    Raises:
        Exception: On API or connection error.
    """

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
    """
    Fetch top screams from a specific archived week.

    Args:
        week_id (str): The identifier for the archived week.

    Returns:
        list: A list of the top 3 scream posts from that week.

    Raises:
        ValueError: If the archive for the given week doesn't exist.
        Exception: For all other failures.
    """

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
    """
    Archive the current week's top screams.

    Args:
        week_id (str): The archive identifier for the week.
        user_id (str): The admin user ID initiating the archive.

    Returns:
        dict: Confirmation of archive status and number of archived screams.

    Raises:
        ValueError: If the archive already exists.
        Exception: On failure to store archive.
    """
    
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

