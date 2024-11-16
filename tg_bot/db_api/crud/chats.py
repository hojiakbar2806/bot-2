from sqlalchemy import select
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.db_api.schemas.chats import Chats


async def select_chat(db: AsyncSession, chat_id: int):
    result = await db.execute(select(Chats).filter(Chats.chat_id == chat_id))
    return result.scalar()


async def register_chat(db: AsyncSession, chat_id: int):
    chat = Chats(chat_id=chat_id)

    try:
        db.add(chat)
        await db.commit()
    except Exception as e:
        print(e)


async def get_chats(db: AsyncSession) -> tuple[int, list[Chats]]:
    result = await db.execute(select(Chats))
    total = await db.execute(text(f"select count(*) from chats"))
    return total.scalar(), result.scalars()


async def delete_chat(db: AsyncSession, user_id: int):
    user = await select_chat(db, user_id)

    try:
        if user is not None:
            await db.delete(user)
            await db.commit()
    except Exception as e:
        print(e)


async def select_list_chats(db: AsyncSession, chats: list[int]):
    users = await db.execute(select(Chats).filter(Chats.chat_id.in_(chats)))
    return users.scalars()
