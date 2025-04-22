import json
from fastapi import HTTPException
import os
import random
import httpx


async def generate_graph_url(data: dict) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://quickchart.io/chart/create",
            json=data
        )
        response.raise_for_status()
        parsed = json.loads(response.text)
        if not parsed['url']:
            error = response.get("error", "Unknown error")
            raise HTTPException(status_code=500, detail=f"Graph generation failed: {error}")
        return parsed["url"]
