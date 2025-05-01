import os
import asyncio
from app_fastapi.tools import archive_top
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
import logging

from app_fastapi.initializers.migration import init_db
from app_fastapi.api import endpoints
from app_fastapi.initializers.engine import engine, get_session
from app_fastapi.models.admin import Admin
from app_fastapi.tools.crypt import hash_user_id
from sqlalchemy import select
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger("app_fastapi")

load_dotenv()

app = FastAPI(
    title="InnoScream API",
    version="1.0.0",
    description="Anonymous student scream platform with memes, reactions, analytics & moderation",
)

@app.on_event("startup")
async def startup():
    try:
        logger.info("Starting application initialization")
        
        await init_db()
        logger.info("Database initialized successfully")

        async for session in get_session():
            user_id = os.getenv("DEFAULT_ADMIN_ID")
            if not user_id:
                logger.warning("DEFAULT_ADMIN_ID not found in .env")
                return

            user_hash = hash_user_id(user_id)
            logger.debug(f"Checking admin for user: {user_id[:5]}...")

            result = await session.execute(select(Admin).where(Admin.user_hash == user_hash))
            admin_exists = result.scalar_one_or_none()

            if admin_exists is None:
                session.add(Admin(user_hash=user_hash))
                await session.commit()
                logger.info(f"Default admin {user_id[:5]}... was added")
            else:
                logger.info(f"Admin {user_id[:5]}... already exists")
        
        scheduler = AsyncIOScheduler()
        scheduler.add_job(
            archive_top,
            'cron',
            day_of_week='sun', 
            hour=23,
            minute=59,
            timezone='UTC'
        )
        scheduler.start()
        logger.info("Scheduler started")
        
        logger.info("Application startup completed successfully")
    except Exception as e:
        logger.critical(f"Application startup failed: {str(e)}", exc_info=True)
        raise
    finally:
        if 'scheduler' in locals() and scheduler.running:
            scheduler.shutdown()

app.include_router(endpoints.router)

if __name__ == "__main__":
    try:
        logger.info("Starting application")
        asyncio.run(init_db())
        uvicorn.run(
            "app_fastapi.main:app", 
            host="0.0.0.0", 
            port=8000, 
            reload=True,
            log_config=None  
        )
    except KeyboardInterrupt:
        logger.info("Application stopped by keyboard interrupt")
    except Exception as e:
        logger.critical(f"Application failed to start: {str(e)}", exc_info=True)
        raise