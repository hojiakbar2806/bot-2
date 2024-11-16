from datetime import datetime

from tg_bot.loader import dp
from tg_bot.db_api.session import SessionLocal
from tg_bot.db_api.crud.users import get_users_with_premium, change_user_premium


async def reset_premium_users():
    async with SessionLocal() as session:
        users = await get_users_with_premium(session)
        time = datetime.now()

        for user in users:
            if time >= user.premium:
                await change_user_premium(session, user.user_id, None)
                await dp.bot.send_message(user.user_id, "<b>Ваша подписка на премиум истекла!</b>")
