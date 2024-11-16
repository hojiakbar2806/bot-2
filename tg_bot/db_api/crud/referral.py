from sqlalchemy import select
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.db_api.schemas.referralurls import ReferralUrls


async def add_referral_url(db: AsyncSession, name: str):
    new = ReferralUrls(name=name)

    try:
        db.add(new)
        await db.commit()
    except Exception as e:
        print(e)


async def get_referral_url(db: AsyncSession, name) -> ReferralUrls:
    query = await db.execute(select(ReferralUrls).filter(ReferralUrls.name == name))
    return query.scalar()


async def delete_referral_url(db: AsyncSession, name):
    ref_url = await get_referral_url(db, name)

    try:
        await db.delete(ref_url)
        await db.commit()
    except Exception as e:
        print(e)


async def get_referral_urls(db: AsyncSession) -> tuple[int, list[ReferralUrls]]:
    query = await db.execute(select(ReferralUrls).order_by(ReferralUrls.users.desc()))
    total = await db.execute(text(f"select count(*) from refurls"))
    return total.scalar(), [x for x in query.scalars()]


async def update_referral_url(db: AsyncSession, name, user_id: int):
    ref_url = await get_referral_url(db, name)
    ref_url.users += [user_id, ]

    try:
        db.add(ref_url)
        await db.commit()
    except Exception as e:
        print(e)


async def update_referral_url_chats(db: AsyncSession, name, chat_id: int):
    ref_url = await get_referral_url(db, name)
    ref_url.chats += [chat_id, ]

    try:
        db.add(ref_url)
        await db.commit()
    except Exception as e:
        print(e)
