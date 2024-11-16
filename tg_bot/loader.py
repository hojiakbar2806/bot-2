from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from tg_bot.config import config


job_stores = dict(default=SQLAlchemyJobStore(config.db.apscheduler_uri))
job_defaults = dict(coalesce=False, max_instances=3)

storage = RedisStorage2(config.redis.host, config.redis.port,
                        db=5, pool_size=10, prefix='bot_fsm')
bot = Bot(config.tgbot.token, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler(timezone="Europe/Moscow",
                             jobstores=job_stores, job_defaults=job_defaults)
bot.config = config
