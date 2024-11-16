from sqlalchemy import select
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.db_api.schemas.payments import Deposits


async def register_deposit(db: AsyncSession, user_id: int, amount: int | float, payment_system: str):
    deposit = Deposits(user_id=user_id, paid=True, payment_system=payment_system, amount=amount)

    try:
        db.add(deposit)
        await db.commit()
        return deposit.id
    except Exception as e:
        print(e)


async def get_user_last_deposit(db: AsyncSession, user_id: int):
    last_deposit = await db.execute(select(Deposits).filter(Deposits.user_id == user_id).order_by(Deposits.amount.desc()))
    return last_deposit.scalar()


async def get_count_deposits(db: AsyncSession):
    total = await db.execute(text(f"select count(*) from deposits"))
    return total.scalar()


async def get_deposits(db: AsyncSession):
    query = await db.execute(select(Deposits))
    return [x for x in query.scalars()]


async def get_sum_amounts(db: AsyncSession):
    total = await db.execute(text(f"select sum(amount) from deposits"))
    return total.scalar()


async def get_max_amount(db: AsyncSession):
    total = await db.execute(text(f"select max(amount) from deposits"))
    return total.scalar()
