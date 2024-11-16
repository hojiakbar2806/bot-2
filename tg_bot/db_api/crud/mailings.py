from sqlalchemy import select
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.db_api.schemas.mailing import Mailing


async def add_mailing(db: AsyncSession, job_id, message_id, message_chat_id, markup, run_date):
    new_mailing = Mailing(job_id=job_id, message_id=message_id, message_chat_id=message_chat_id,
                          markup=markup, run_date=run_date)

    try:
        db.add(new_mailing)
        await db.commit()
    except Exception as e:
        print(e)


async def get_mailing(db: AsyncSession, job_id) -> Mailing:
    query = await db.execute(select(Mailing).filter(Mailing.job_id == job_id))
    return query.scalar()


async def delete_mailing(db: AsyncSession, job_id):
    mailing = await get_mailing(db, job_id)

    try:
        await db.delete(mailing)
        await db.commit()
    except Exception as e:
        print(e)


async def get_mailings(db: AsyncSession) -> tuple[int, list[Mailing]]:
    query = await db.execute(select(Mailing).order_by(Mailing.run_date.asc()))
    total = await db.execute(text(f"select count(*) from mailings"))
    return total.scalar(), [x for x in query.scalars()]


async def get_mailing_by_message_id(db: AsyncSession, message_id) -> Mailing:
    query = await db.execute(select(Mailing).filter(Mailing.message_id == message_id))
    return query.scalar()


async def end_mailing_by_message_id(db: AsyncSession, message_id,
                                    active: bool,
                                    total: int,
                                    success: int,
                                    failed: int):
    mailing = await get_mailing_by_message_id(db, message_id)

    mailing.active = active
    mailing.total = total
    mailing.success = success
    mailing.failed = failed

    try:
        db.add(mailing)
        await db.commit()
    except Exception as e:
        print(e)
