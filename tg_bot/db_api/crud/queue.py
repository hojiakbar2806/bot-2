from sqlalchemy import select, or_
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.db_api.schemas.queue import Queue


async def get_user_in_queue(db: AsyncSession, user_id: int):
    result = await db.execute(select(Queue).filter(Queue.user_id == user_id))
    return result.scalar()


async def add_user_in_queue(db: AsyncSession, user_id: int, sex, opposite_sex, age):
    user_queue = Queue(user_id=user_id, sex=sex, opposite_sex=opposite_sex, age=age)

    try:
        db.add(user_queue)
        await db.commit()
    except:
        pass


async def select_user_from_queue(db: AsyncSession, user_id: int, sex):
    user = await db.execute(
        select(Queue)
        .filter(
            Queue.user_id != user_id,
            or_(Queue.opposite_sex == sex, Queue.opposite_sex == "any")
        )
    )
    return user.scalar()


async def delete_user_from_queue(db: AsyncSession, user_id):
    user = await get_user_in_queue(db, user_id)

    try:
        if user is not None:
            await db.delete(user)
            await db.commit()
    except:
        pass
