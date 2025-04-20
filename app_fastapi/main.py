import asyncio

from fastapi import FastAPI
import uvicorn

from app_fastapi.initializers.migration import init_db
from app_fastapi.api import endpoints


app = FastAPI(
    title="InnoScream API",
    version="1.0.0",
    description="Anonymous student scream platform with memes, reactions, analytics & moderation",
)


@app.on_event("startup")
async def startup():
    await init_db()


app.include_router(endpoints.router)


if __name__ == "__main__":
    asyncio.run(init_db())
    uvicorn.run("app_fastapi.main:app", host="0.0.0.0", port=8000, reload=True)
