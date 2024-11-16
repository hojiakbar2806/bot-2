from sqlalchemy import select
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.db_api.schemas.user import User


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.user_id == user_id))
    return result.scalar()


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalar()


async def register_user(db: AsyncSession, user_id: int,
                        username: str | None, full_name: str | None,
                        referral_id: int | None, registered: bool,
                        place, sex, age):
    user = User(user_id=user_id, username=username, full_name=full_name, referral_id=referral_id,
                registered=registered, sex=sex, age=age, place=place)

    try:
        db.add(user)
        await db.commit()
    except Exception as e:
        print(e)


async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    total = await db.execute(text(f"select count(*) from users"))
    return total.scalar(), result.scalars()


async def get_referred_users(db: AsyncSession):
    result = await db.execute(select(User).filter(User.referral_id != 0))
    total = await db.execute(text(f"select count(*) from users where referral_id != 0"))
    return total.scalar(), result.scalars()


async def get_registered_users(db: AsyncSession):
    result = await db.execute(select(User).filter(User.registered == True))
    total = await db.execute(text(f"select count(*) from users where registered = True"))
    return total.scalar(), result.scalars()


async def get_count_required_subs_users(db: AsyncSession):
    total = await db.execute(text(f"select count(*) from users where place = 'channel'"))
    return total.scalar()


async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user(db, user_id)

    try:
        if user is not None:
            await db.delete(user)
            await db.commit()
    except Exception as e:
        print(e)


async def change_ban_user(db: AsyncSession, user_id: int, value: bool):
    user = await get_user(db, user_id)
    user.ban = value

    try:
        db.add(user)
        await db.commit()
    except Exception as e:
        print(e)


async def select_list_users(db: AsyncSession, users: list[int]):
    users = await db.execute(select(User).filter(User.user_id.in_(users)))
    return users.scalars()


async def change_user_balance(db: AsyncSession, user_id: int, amount: int | float):
    user = await get_user(db, user_id)

    user.balance += amount

    try:
        db.add(user)
        await db.commit()
    except Exception as e:
        print(e)


async def change_user_sex(db: AsyncSession, user_id: int, sex):
    user = await get_user(db, user_id)

    user.sex = sex

    try:
        db.add(user)
        await db.commit()
    except Exception as e:
        print(e)


async def change_user_age(db: AsyncSession, user_id: int, age):
    user = await get_user(db, user_id)

    user.age = age

    try:
        db.add(user)
        await db.commit()
    except Exception as e:
        print(e)


async def change_user_registered(db: AsyncSession, user_id: int, value):
    user = await get_user(db, user_id)

    user.registered = value

    try:
        db.add(user)
        await db.commit()
    except Exception as e:
        print(e)


async def add_total_dialogs(db: AsyncSession, user_id: int):
    user = await get_user(db, user_id)

    user.total_dialogs += 1

    try:
        db.add(user)
        await db.commit()
    except Exception as e:
        print(e)


async def add_total_messages(db: AsyncSession, user_id: int):
    user = await get_user(db, user_id)

    user.total_messages += 1

    try:
        db.add(user)
        await db.commit()
    except Exception as e:
        print(e)


async def change_user_premium(db: AsyncSession, user_id: int, date):
    user = await get_user(db, user_id)

    user.premium = date

    try:
        db.add(user)
        await db.commit()
    except Exception as e:
        print(e)


async def get_users_with_premium(db: AsyncSession):
    users = await db.execute(select(User).filter(User.premium != None))
    return users.scalars()


async def change_user_opposite_sex(db: AsyncSession, user_id: int, opposite_sex):
    user = await get_user(db, user_id)

    user.opposite_sex = opposite_sex

    try:
        db.add(user)
        await db.commit()
    except Exception as e:
        print(e)
