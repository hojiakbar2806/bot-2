from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.utils.parts import paginate

from tg_bot.db_api.crud.required_subs import get_required_subs


continue_markup = InlineKeyboardMarkup()
continue_markup.add(
    InlineKeyboardButton("➡️ Продолжить", callback_data="req_sub:continue")
).add(
    InlineKeyboardButton("🔄 Ввести другой", callback_data="req_sub:refresh")
)


verify_markup = InlineKeyboardMarkup()
verify_markup.add(
    InlineKeyboardButton("✅ Проверять", callback_data="req_sub:verify:yes"),
).add(
    InlineKeyboardButton("🚫 Не проверять", callback_data="req_sub:verify:no"),
)

required_markup = InlineKeyboardMarkup()
required_markup.add(
    InlineKeyboardButton("📈 Активные каналы", callback_data="req_sub:stats")
).add(
    InlineKeyboardButton("*️⃣ Добавить", callback_data="req_sub:create")
).add(
    InlineKeyboardButton("◀️ Назад", callback_data="admin:mailing_md")
)


async def paginate_subs_markup(db: AsyncSession, page: int):
    count_subs, required_subs = await get_required_subs(db)
    keyboard = InlineKeyboardMarkup()
    total_page = int(count_subs/10)
    data = "req_sub:pg:"
    buttons = paginate(required_subs, page=page, limit=10)

    for sub in buttons:
        smile = "🚫" if sub.verify is False else "✅"
        text = f"[{smile}] 🗃 {sub.channel_url}"
        keyboard.add(InlineKeyboardButton(text, callback_data=f"req:sub:{sub.sid}"))

    if page + 1 <= total_page:
        keyboard.add(InlineKeyboardButton("▶️ Дальше", callback_data=data + f"{page+1}"))
    if page - 1 >= 0:
        keyboard.add(InlineKeyboardButton("◀️ Назад", callback_data=data + f"{page-1}"))

    keyboard.add(
        InlineKeyboardButton(f"👀 {page + 1}/{total_page+1}", callback_data="none"),
        InlineKeyboardButton("◀️ Назад в меню", callback_data="admin:mailing_md"))

    return keyboard


def channel_markup(channel_id: int, verify: bool):
    keyboard = InlineKeyboardMarkup()

    verify_button =\
        InlineKeyboardButton("#️⃣ Выключить проверку", callback_data=f"rq:verify:off:{channel_id}") \
        if verify is True else \
        InlineKeyboardButton("⏺ Включить проверку", callback_data=f"rq:verify:on:{channel_id}")

    keyboard.add(InlineKeyboardButton("🔗 Изменить ссылку", callback_data=f"rq:change_url:{channel_id}"))
    keyboard.add(InlineKeyboardButton("🚫 Удалить", callback_data=f"rq:delete:{channel_id}"))
    keyboard.add(verify_button)
    keyboard.add(InlineKeyboardButton("◀️ Назад", callback_data="req_sub:pg:0"))

    return keyboard


def confirm_delete_markup(channel_id: int):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("❌ Удалить", callback_data=f"req:delete:{channel_id}"))
    keyboard.add(InlineKeyboardButton("🙅🏻‍♂️ Не удалять", callback_data=f"req:cancel_delete"))
    return keyboard
