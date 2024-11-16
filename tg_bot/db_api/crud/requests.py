from sqlalchemy import select
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.db_api.schemas.requests import Requests


async def add_request(db: AsyncSession, channel_id: int, post: int, chat_id: int,
                      reply_markup: dict | None, accept: bool):
    new_request = Requests(channel_id=channel_id, message_id=post, message_chat_id=chat_id,
                           accept_request=accept, reply_markup=reply_markup)

    try:
        db.add(new_request)
        await db.commit()
    except Exception as e:
        print(e)


async def select_request(db: AsyncSession, channel_id: int) -> Requests:
    query = await db.execute(
        select(Requests)
        .filter(Requests.channel_id == channel_id))
    return query.scalar()


async def delete_request(db: AsyncSession, channel_id: int):
    request = await select_request(db, channel_id)

    try:
        await db.delete(request)
        await db.commit()
    except Exception as e:
        print(e)


async def get_requests(db: AsyncSession) -> tuple[int, list[Requests]]:
    query = await db.execute(select(Requests))
    total = await db.execute(
        text(f"select count(*) from requests"))
    return total.scalar(), [x for x in query.scalars()]


async def change_accept_request(db: AsyncSession, chat_id: int, value: bool):
    request = await select_request(db, chat_id)
    request.accept_request = value

    try:
        db.add(request)
        await db.commit()
    except Exception as e:
        print(e)


async def change_post_request(db: AsyncSession, channel_id, message_chat_id,
                              message_id, reply_markup):
    request = await select_request(db, channel_id)

    request.message_id = message_id
    request.message_chat_id = message_chat_id
    request.reply_markup = reply_markup

    try:
        db.add(request)
        await db.commit()
    except Exception as e:
        print(e)
