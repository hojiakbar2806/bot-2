from sqlalchemy import select
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.db_api.schemas.requiredsub import RequiredSub


async def add_required_sub(db: AsyncSession, channel_id: int,  url: str, verify: bool):
    new_sub = RequiredSub(channel_id=channel_id, channel_url=url, verify=verify)

    try:
        db.add(new_sub)
        await db.commit()
    except Exception as e:
        print(e)


async def get_required_sub(db: AsyncSession, channel_id) -> RequiredSub:
    query = await db.execute(select(RequiredSub).filter(RequiredSub.channel_id == channel_id))
    return query.scalar()


async def get_required_sub_by_sid(db: AsyncSession, sid) -> RequiredSub:
    query = await db.execute(select(RequiredSub).filter(RequiredSub.sid == sid))
    return query.scalar()


async def delete_sub(db: AsyncSession, channel_id):
    req_sub = await get_required_sub(db, channel_id)

    try:
        await db.delete(req_sub)
        await db.commit()
    except Exception as e:
        print(e)


async def delete_sub_by_sid(db: AsyncSession, sid):
    req_sub = await get_required_sub_by_sid(db, sid)

    try:
        await db.delete(req_sub)
        await db.commit()
    except Exception as e:
        print(e)


async def get_required_subs(db: AsyncSession) -> tuple[int, list[RequiredSub]]:
    query = await db.execute(select(RequiredSub))
    total = await db.execute(text(f"select count(*) from required_subs"))
    return total.scalar(), [x for x in query.scalars()]


async def get_mailings_verified(db: AsyncSession) -> list[RequiredSub]:
    query = await db.execute(
        select(RequiredSub)
        .filter(RequiredSub.verify == True)
    )
    return [x for x in query.scalars()]


async def change_sub_verify(db: AsyncSession, chat_id: int, value: bool):
    sub = await get_required_sub(db, chat_id)
    sub.verify = value

    try:
        db.add(sub)
        await db.commit()
    except Exception as e:
        print(e)


async def change_sub_verify_by_sid(db: AsyncSession, sid: int, value: bool):
    sub = await get_required_sub_by_sid(db, sid)
    sub.verify = value

    try:
        db.add(sub)
        await db.commit()
    except Exception as e:
        print(e)


async def change_sub_url(db: AsyncSession, chat_id: int, url: bool):
    sub = await get_required_sub(db, chat_id)
    sub.channel_url = url

    try:
        db.add(sub)
        await db.commit()
    except Exception as e:
        print(e)


async def change_sub_url_by_sid(db: AsyncSession, sid: int, url: bool):
    sub = await get_required_sub_by_sid(db, sid)
    sub.channel_url = url

    try:
        db.add(sub)
        await db.commit()
    except Exception as e:
        print(e)


async def add_sub_users(db: AsyncSession, channel_url: int, user_id: int):
    sub = await get_required_sub(db, channel_url)
    if user_id not in sub.users_subbed:
        sub.users_subbed += [user_id, ]

        try:
            db.add(sub)
            await db.commit()
        except Exception as e:
            print(e)


async def delete_sub_users(db: AsyncSession, channel_url: int, user_id: int):
    sub = await get_required_sub(db, channel_url)
    if user_id in sub.users_subbed:
        sub.users_subbed.remove(user_id)

        try:
            db.add(sub)
            await db.commit()
        except Exception as e:
            print(e)


async def select_user_in_sub(db: AsyncSession, channel_url: int, user_id: int):
    sub = await get_required_sub(db, channel_url)
    return True if user_id in sub.users_subbed else False
