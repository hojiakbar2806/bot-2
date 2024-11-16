from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.utils.parts import paginate

from tg_bot.db_api.crud.mailings import get_mailings


pin_markup = InlineKeyboardMarkup()
pin_markup.add(
    InlineKeyboardButton("📌 Закреплять", callback_data="mailing:pin:on")
).add(
    InlineKeyboardButton("🚫 Не закреплять", callback_data="mailing:pin:off")
)


def delete_mail_markup(job_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("❌ Удалить рассылку", callback_data=f"mailing_job:delete:{job_id}")
    )
    return keyboard


async def paginate_mailing_markup(db: AsyncSession, page: int):
    count_mailing, mailings = await get_mailings(db)
    keyboard = InlineKeyboardMarkup()
    total_page = int(count_mailing/10)
    data = "ml:pg:"

    buttons = paginate(mailings, page=page, limit=10)

    for mailing in buttons:
        smile = "🚫" if mailing.active is True else "✅"
        text = f"[{smile}] {mailing.run_date.strftime('%d.%m.%Y %H:%M')}"
        keyboard.add(InlineKeyboardButton(text, callback_data=f"ml:job:{mailing.job_id}"))

    if page + 1 <= total_page:
        keyboard.add(InlineKeyboardButton("▶️ Дальше", callback_data=data + f"{page+1}"))
    if page - 1 >= 0:
        keyboard.add(InlineKeyboardButton("◀️ Назад", callback_data=data + f"{page-1}"))

    keyboard.add(
        InlineKeyboardButton(f"👀 {page + 1}/{total_page+1}", callback_data="none"),
        InlineKeyboardButton("◀️ Назад в меню", callback_data="admin:mailing_md"))

    return keyboard


async def mail_markup(job_id):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton("👁 Посмотреть пост", callback_data=f"ml:view_post:{job_id}")
    ).add(
        InlineKeyboardButton("❌ Удалить", callback_data=f"mailing_job:delete:{job_id}")
    ).add(
        InlineKeyboardButton("◀️ Назад", callback_data="ml:pg:0")
    )

    return keyboard


def current_mail_markup(job_id: str):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton("🔄 Обновить", callback_data=f"mail:update:{job_id}")
    )
    return keyboard
