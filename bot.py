import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import handlers
from database import database as db
import time

async def on_startup():
    db.create_users_table()
    db.create_sources_table()
    db.create_news_table()
    db.create_news_gpt_table()
    db.clear_news_table()
    db.clear_news_gpt()

async def main():
    # Конфигурируем логирование
    logging.basicConfig(
      level=logging.DEBUG,
      format='%(filename)s:%(lineno)d #%(levelname)-8s '
             '[%(asctime)s] - %(name)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.info('Starting bot')
    bot = Bot(token='6737680398:AAHoNncM8dISG55i-x4YsvzvAqd5eqeXVWI',
              parse_mode='HTML')
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.include_routers(handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
