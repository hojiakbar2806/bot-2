import asyncio
import json

from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tg_bot.db_api.session import SessionLocal

from tg_bot.db_api.crud.users import get_users
from tg_bot.db_api.crud.chats import get_chats
from tg_bot.db_api.crud.mailings import end_mailing_by_message_id, get_mailing_by_message_id
from tg_bot.loader import dp
from tg_bot.keyboards.admin.inline.mailing import current_mail_markup
from tg_bot.utils.settings import parse_settings


async def mailing_users(message, pin):
    settings = parse_settings()
    keyboard = \
        InlineKeyboardMarkup(inline_keyboard=json.loads(message["reply_markup"])["inline_keyboard"]) \
        if message["reply_markup"] is not None \
        else InlineKeyboardMarkup()
    start_time = datetime.now()
    success, failed = 0, 0

    if settings["buttons"]["buy"]["active"] is True:
        try:
            keyboard.add(InlineKeyboardButton("💳 Купить", url=settings['buttons']['buy']['url']))
        except:
            pass

    if settings['buttons']['hide'] is True:
        keyboard.add(InlineKeyboardButton("❌ Скрыть", callback_data='hide_message'))

    if keyboard.inline_keyboard is not None:
        keyboard = keyboard
    else:
        keyboard = None

    async with SessionLocal() as session:
        mailing = await get_mailing_by_message_id(session, message["message_id"])
        count, users = await get_users(session)

        await dp.bot.send_message(
            dp.bot.config.owner_id,
            f"<b>📧 Рассылка на {start_time} была запущена!</b>\n"
            f"<b>· Всего: {success + failed}</b>\n"
            f"<b>· Успешно: {success}</b>\n"
            f"<b>· Не доставлено: {failed}</b>\n",
            reply_markup=current_mail_markup(mailing.job_id)
        )

        for user in users:
            try:
                u_msg = await dp.bot.copy_message(user.user_id,
                                                  message["chat"]["id"],
                                                  message["message_id"],
                                                  reply_markup=keyboard)

                if pin is True:
                    await dp.bot.pin_chat_message(user.user_id, u_msg.message_id)

                success += 1
            except:
                failed += 1

            await end_mailing_by_message_id(session, int(message["message_id"]), True,
                                            success + failed, success, failed)

            await asyncio.sleep(.1)

        end_time = datetime.now()
        time_spent = end_time - start_time

        await dp.bot.send_message(
            dp.bot.config.owner_id,
            "<b>📧 Рассылка прошла успешно!</b>\n"
            f"<b>🫂 Всего: {success + failed}</b>\n"
            f"<b>· Успешно: {success}</b>\n"
            f"<b>· Не доставлено: {failed}</b>\n\n"
            f"<b>🕐 Время начала: {start_time}</b>\n"
            f"<b>⏳ Затраченное время: {time_spent}</b>"
        )
        await end_mailing_by_message_id(session, int(message["message_id"]), False,
                                        success + failed, success, failed)


async def mailing_chats(message, pin):
    settings = parse_settings()
    keyboard = \
        InlineKeyboardMarkup(inline_keyboard=message["reply_markup"]["inline_keyboard"]) \
        if message["reply_markup"] is not None \
        else InlineKeyboardMarkup()

    if settings["buttons"]["buy"]["active"] is True:
        try:
            keyboard.add(InlineKeyboardButton("💳 Купить", url=settings['buttons']['buy']['url']))
        except:
            pass

    if settings['buttons']['hide'] is True:
        keyboard.add(InlineKeyboardButton("❌ Скрыть", callback_data='hide_message'))

    start_time = datetime.now()
    success, failed = 0, 0
    async with SessionLocal() as session:
        mailing = await get_mailing_by_message_id(session, message["message_id"])
        count, chats = await get_chats(session)

        await dp.bot.send_message(
            dp.bot.config.owner_id,
            f"<b>📧 Рассылка на {start_time} была запущена!</b>\n"
            f"<b>· Всего: {success + failed}</b>\n"
            f"<b>· Успешно: {success}</b>\n"
            f"<b>· Не доставлено: {failed}</b>\n",
            reply_markup=current_mail_markup(mailing.job_id)
        )

        for chat in chats:
            try:
                u_msg = await dp.bot.copy_message(chat.chat_id,
                                                  message["chat"]["id"],
                                                  message["message_id"],
                                                  reply_markup=keyboard)

                if pin is True:
                    await dp.bot.pin_chat_message(chat.chat_id, u_msg.message_id)

                success += 1
            except:
                failed += 1

            await end_mailing_by_message_id(session, int(message["message_id"]), True,
                                            success + failed, success, failed)

            await asyncio.sleep(.1)

        end_time = datetime.now()
        time_spent = end_time - start_time

        await dp.bot.send_message(
            dp.bot.config.owner_id,
            "<b>📧 Рассылка успешно прошла!</b>\n"
            f"<b>· Всего: {success + failed}</b>\n"
            f"<b>· Успешно: {success}</b>\n"
            f"<b>· Не доставлено: {failed}</b>\n\n"
            f"<b>🕐 Время начала: {start_time}</b>\n"
            f"<b>⏳ Затраченное время: {time_spent}</b>"
        )
        await end_mailing_by_message_id(session, int(message["message_id"]), False,
                                        success + failed, success, failed)
