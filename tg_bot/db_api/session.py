from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from tg_bot.config import config
from tg_bot.utils.logger import logger

engine = create_async_engine(config.db.db_uri, pool_pre_ping=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False,
                            autocommit=False, autoflush=False,)
Base = declarative_base()


async def create_db_and_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        logger.error(e)
