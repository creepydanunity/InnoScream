# Standard library
import asyncio
import os

# Third‑party
from aiogram import Bot, Dispatcher

# Local application
from app_bot.handlers.adminHandler import adminRouter
from app_bot.handlers.getIdHandler import idRouter
from app_bot.handlers.historyHandler import historyRouter
from app_bot.handlers.reactionHandler import reactionRouter
from app_bot.handlers.startHandler import startRouter
from app_bot.handlers.screamHandler import screamRouter
from app_bot.handlers.statsHandler import statsRouter
from app_bot.logger import logger


async def main():
    """
    Initialize and start the Telegram bot.

    Behavior:
        - Loads the bot token from environment variable.
        - Sets up the Dispatcher and registers all route handlers.
        - Starts polling for new updates with a 120-second timeout.
        - Logs the initialization process and any critical failures.

    Routers included:
        - historyRouter: Handles archive-related commands.
        - reactionRouter: Manages user reactions to screams.
        - screamRouter: Handles scream submission and feed browsing.
        - statsRouter: Provides user statistics.
        - adminRouter: Handles admin commands (delete, confirm, etc.).
        - idRouter: Returns the user's ID.
        - startRouter: Welcome users and explains bot functionality.

    Raises:
        Exception: If initialization or polling fails.
    """
    try:
        logger.info("Initializing bot")
        bot = Bot(token=os.getenv("BOT_TOKEN"))
        dp = Dispatcher()
        dp.include_router(historyRouter)
        dp.include_router(reactionRouter)
        dp.include_router(screamRouter)
        dp.include_router(statsRouter)
        dp.include_router(adminRouter)
        dp.include_router(idRouter)
        dp.include_router(startRouter)
        logger.info("All routers included")
        logger.info("Starting polling")
        await dp.start_polling(bot, polling_timeout=120, skip_updates=False)
    except Exception as e:
        logger.critical(f"Bot failed to start: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by keyboard interrupt")
    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}", exc_info=True)
