import asyncio
import multiprocessing
from aiogram import Bot, Dispatcher
from handlers import bot_commands, bot_user_messages, callback
from middlewares.throttle import AntiFloodMiddleware
from config import config as cfg
from db_models import Base, engine

async def main_bot():
    bot = Bot(cfg.bot_token)
    dp = Dispatcher()
    await bot.set_my_commands(bot_commands.commands)

    dp.message.middleware(AntiFloodMiddleware(0.5))

    dp.include_routers(
        bot_user_messages.router,
        bot_commands.router,
        callback.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

def start_bot():
    asyncio.run(main_bot())

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    bot_process = multiprocessing.Process(target=start_bot)
    bot_process.start()
    bot_process.join()
