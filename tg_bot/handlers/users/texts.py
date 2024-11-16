from aiogram.types import Message, ChatType
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.loader import dp
from tg_bot.keyboards.users.inline import premium_markup, buy_premium_markup
from tg_bot.db_api.crud.users import get_user
from tg_bot.utils.settings import parse_settings


@dp.message_handler(commands="rules", chat_type=ChatType.PRIVATE)
@dp.message_handler(text="📕 Правила", chat_type=ChatType.PRIVATE)
async def rules_handler(message: Message):
    await message.answer("<i>📌 Правила общения в анонимном чате:\n\n"
                         "1. Любые упоминания психоактивных веществ (наркотиков)\n"
                         "2. Обсуждение политики\n"
                         "3. Детская порнография ('ЦП')\n"
                         "4. Мошенничество (Scam)\n"
                         "5. Любая реклама, спам\n"
                         "6. Рассовая, половая, сексуальная, и любая другая дискриминация\n"
                         "7. Продажи чего либо (например - продажа интимных фотографий, видео)\n"
                         "8. Любые действия, нарушающие правила Telegram\n"
                         "9. Оскорбительное поведение\n\n"
                         "<b>❌ За нарушение правил - блокировка аккаунта</b></i>")


@dp.message_handler(commands="prem", chat_type=ChatType.PRIVATE)
@dp.message_handler(text="👑 Premium статус", chat_type=ChatType.PRIVATE)
async def premium_handler(message: Message, session: AsyncSession):
    user = await get_user(session, message.from_user.id)

    premium_settings = parse_settings()["premium"]

    if user.premium is None:
        await message.answer(
            "<i><b>👑 Получите Premium-статус: </b>\n\n"
            "🔍 Ищите по полу (м/ж, 18+)\n"
            "📱 Полное отключение рекламы</i>",
            reply_markup=buy_premium_markup(
                premium_settings["day"],
                premium_settings["week"],
                premium_settings["month"],
                premium_settings["all"])
        )
    else:
        await message.answer(
            f"<b>👑 Premium-статус активен до {user.premium.strftime('%d.%m.%Y %H:%M')}</b>",
            reply_markup=premium_markup)


@dp.message_handler(commands="profile", chat_type=ChatType.PRIVATE)
@dp.message_handler(text="👨‍💻 Профиль", chat_type=ChatType.PRIVATE)
async def profile_handler(message: Message, session: AsyncSession):
    user = await get_user(session, message.from_user.id)

    smile = "🙎‍♂" if user.sex == "man" else "🙍‍♀"
    sex = "М" if user.sex == "man" else "Ж"
    premium = "Есть" if user.premium is not None else "Нет"

    await message.answer(
        f"<b>👤 Мой профиль</b> (<code>{message.from_user.id}</code>)\n\n"
        f"<b>{smile} Пол</b>: <code>{sex}</code>\n"
        f"<b>🔞 Возраст</b>: <code>{user.age}</code>\n\n"
        f"<b>👑 Премиум-статус:</b> <code>{premium}</code>\n\n"
        f"<b>📫 Всего диалогов:</b> <code>{user.total_dialogs}</code>\n"
        f"<b>📤 Всего сообщений:</b> <code>{user.total_messages}</code>"
    )
