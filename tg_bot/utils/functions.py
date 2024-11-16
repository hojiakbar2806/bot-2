import aiofiles
import os


from pyqiwip2p import AioQiwiP2P
from aiogram import Bot, Dispatcher
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from tg_bot.config import config
from tg_bot.db_api.crud.users import get_users
from tg_bot.db_api.crud.required_subs import get_mailings_verified, get_required_subs, \
    add_sub_users, delete_sub_users
from tg_bot.keyboards.users.inline import subscribe_markup
from tg_bot.services.payments.qiwi_pay import payment_history_last
from tg_bot.services.payments.lolz_pay import Lolz
from tg_bot.services.payments.crystal_pay import CrystalPay
from tg_bot.services.botstat.api import BotStats


async def dump_users_to_file(db: AsyncSession):
    async with aiofiles.open("users.txt", "w", encoding="utf-8") as file:
        _text = ""
        _, users = await get_users(db)

        for user in users:
            _text += str(user.user_id) + "\n"

        await file.write(_text)

    return "users.txt"


async def check_sub(bot: Bot, user_id: int, session):
    verify = []
    verify_channels = await get_mailings_verified(session)
    _, all_channels = await get_required_subs(session)
    markup = await subscribe_markup(all_channels)

    for channel in verify_channels:
        try:
            status = await bot.get_chat_member(channel.channel_id, user_id)

            if status.status != "left":
                verify.append(True)
                print(verify)
                await add_sub_users(session, channel.channel_id, user_id)
            else:
                verify.append(False)
                await delete_sub_users(session, channel.channel_id, user_id)
        except Exception as e:
            print(e)
            verify.append(True)

    return markup, all(verify)


async def get_users_from_file(file_path: str):
    async with aiofiles.open(file_path, "r") as file:
        try:
            file_text = await file.read()
            return [int(x) for x in file_text.splitlines()]
        except:
            return []


async def validate_block_bot(dp: Dispatcher, users: list[int]):
    dead_users = []
    alive_users = []

    for user in users:
        try:
            await dp.bot.send_chat_action(user, "typing")
            alive_users.append(user)
        except:
            dead_users.append(user)

    return dead_users, alive_users


def count_users(users):
    week, day, hour, today, month = \
        timedelta(weeks=1), timedelta(days=1), \
        timedelta(hours=1), datetime.now(), timedelta(weeks=4)
    counts = {"week": 0, "day": 0, "hour": 0, "month": 0}

    for user in users:
        if today - user.registration_date <= week:
            counts["week"] += 1
        if today - user.registration_date <= day:
            counts["day"] += 1
        if today - user.registration_date <= hour:
            counts["hour"] += 1
        if today - user.registration_date <= month:
            counts["month"] += 1

    return counts["week"], counts["day"], counts["hour"], counts["month"]


def count_payments(payments):
    week, day, hour, today, month = \
        timedelta(weeks=1), timedelta(days=1), \
        timedelta(hours=1), datetime.now(), timedelta(weeks=4)
    counts = {"week": 0, "day": 0, "hour": 0, "month": 0}

    for user in payments:
        if today - user.date <= week:
            counts["week"] += 1
        if today - user.date <= day:
            counts["day"] += 1
        if today - user.date <= hour:
            counts["hour"] += 1
        if today - user.date <= month:
            counts["month"] += 1

    return counts["week"], counts["day"], counts["hour"], counts["month"]


async def send_to_bot_safe(db: AsyncSession):
    await dump_users_to_file(db)

    with open("users.txt", "rb") as file:
        async with BotStats(config.tgbot.token,
                            config.bot_stat.access_token) as api:
            response = await api.create_task(file, config.tgbot.token)

    os.remove("users.txt")
    return response


async def send_to_bot_man(db: AsyncSession):
    await dump_users_to_file(db)

    with open("users.txt", "rb") as file:
        async with BotStats(config.tgbot.token,
                            config.bot_stat.access_token) as api:
            response = await api.send_to_botman(config.tgbot.token, config.owner_id, file)

    os.remove("users.txt")
    return response


async def check_service_stable(call, service: str):
    match service:
        case "qiwi_p2p":
            try:
                _ = AioQiwiP2P(call.bot.config.payments.qiwi.qiwi_p2p.token)
                text = "<b>Токен работает</b>"
            except:
                text = "<b>Токен не работает</b>"

            return text

        case "lolz_pay":
            try:
                async with Lolz(call.bot.config.payments.lolz.api_key) as _:
                    pass
                text = "<b>Токен работает</b>"
            except Exception as e:
                print(e)
                text = "<b>Токен не работает</b>"

            return text

        case "crystal_pay":
            try:
                async with CrystalPay(call.bot.config.payments.crystalpay.name,
                                      call.bot.config.payments.crystalpay.secret_key) as _:
                    info = await _.get_me()
                    print(info)
                text = "<b>Токен работает</b>"
            except Exception as e:
                print(e)
                text = "<b>Токен не работает</b>"

            return text

        case "qiwi_api":
            try:
                await payment_history_last(
                    call.bot.config.payments.qiwi.qiwi_api.phone[1:],
                    call.bot.config.payments.qiwi.qiwi_api.token
                )
                text = "<b>Токен работает</b>"
            except:
                text = "<b>Токен не работает</b>"

            return text
