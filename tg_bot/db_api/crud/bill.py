from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.db_api.schemas.payments import Bill


async def select_bill(db: AsyncSession, bill_id: int) -> Bill:
    result = await db.execute(select(Bill).filter(Bill.bill_id == bill_id))
    return result.scalar()


async def register_bill(db: AsyncSession, user_id: int, amount: int | float):
    bill = Bill(user_id=user_id, amount=amount, comment=f"bill_{user_id}")

    try:
        db.add(bill)
        await db.commit()
        return bill.bill_id
    except Exception as e:
        print(e)
