from sqlalchemy import select, or_
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.db_api.schemas.rooms import Room


async def get_user_in_room(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Room)
        .filter(
            or_(
                Room.first_user_id == user_id,
                Room.second_user_id == user_id
            )
        )
    )
    return result.scalar()


async def add_new_room(db: AsyncSession, first_user_id: int, second_user_id: int):
    room = Room(first_user_id=first_user_id, second_user_id=second_user_id)

    try:
        db.add(room)
        await db.commit()
    except:
        pass


async def delete_room(db: AsyncSession, room_id: int):
    room = await db.execute(select(Room).filter(Room.room_id == room_id))
    room = room.scalar()

    try:
        if room is not None:
            await db.delete(room)
            await db.commit()
    except:
        pass

