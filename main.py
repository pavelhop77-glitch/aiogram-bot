import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers.routes import router, notifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не задан в .env")

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(router)


async def main():
    logger.info("Start bot...")
    
    asyncio.create_task(notifier(bot))
    
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())