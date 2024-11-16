from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.utils.parts import paginate

from tg_bot.db_api.crud.requests import get_requests


admins_markup = InlineKeyboardMarkup()
admins_markup.add(
    InlineKeyboardButton("*️⃣ Добавить", callback_data="admin:admins:add"),
    InlineKeyboardButton("❌ Удалить", callback_data="admin:admins:delete"),
).add(
    InlineKeyboardButton("◀️ Назад", callback_data="admin:settings")
)

requests_markup = InlineKeyboardMarkup()
requests_markup.add(
    InlineKeyboardButton("🗄 Активные каналы", callback_data="admin:requests:active")
).add(
    InlineKeyboardButton("*️⃣ Добавить канал", callback_data="admin:requests:add")
).add(
    InlineKeyboardButton("❌ Удалить канал", callback_data="admin:requests:delete")
).add(
    InlineKeyboardButton("◀️ Назад", callback_data="admin:settings")
)


def backup_markup(files, users, auto):
    keyboard = InlineKeyboardMarkup()

    files_button = InlineKeyboardButton("#️⃣ Выключить бэкап файлов", callback_data="backup:files:off") \
        if files is True else \
        InlineKeyboardButton("⏺ Включить бэкап файлов", callback_data="backup:files:on")

    users_button = InlineKeyboardButton("#️⃣ Выключить бэкап юзеров", callback_data="backup:users:off") \
        if users is True else \
        InlineKeyboardButton("⏺ Включить бэкап юзеров", callback_data="backup:users:on")

    auto_button = InlineKeyboardButton("#️⃣ Выключить авто-бэкап", callback_data="backup:auto:off") \
        if auto is True else \
        InlineKeyboardButton("⏺ Включить авто-бэкап", callback_data="backup:auto:on")

    keyboard.add(files_button)
    keyboard.add(users_button)
    keyboard.add(auto_button)
    keyboard.add(
        InlineKeyboardButton("◀️ Назад", callback_data="admin:settings"))

    return keyboard


def botstat_markup(auto_update: bool):
    keyboard = InlineKeyboardMarkup()

    auto_button = InlineKeyboardButton("#️⃣ Выключить авто-обновление", callback_data="botstat:auto:off") \
        if auto_update is True else \
        InlineKeyboardButton("⏺ Включить авто-обновление", callback_data="botstat:auto:on")

    keyboard.add(auto_button)
    keyboard.add(InlineKeyboardButton("◀️ Назад", callback_data="admin:settings"))

    return keyboard


continue_markup = InlineKeyboardMarkup()
continue_markup.add(
    InlineKeyboardButton("➡️ Продолжить", callback_data="requests:continue")
).add(
    InlineKeyboardButton("🔄 Ввести другой", callback_data="requests:refresh")
)

accept_markup = InlineKeyboardMarkup()
accept_markup.add(
    InlineKeyboardButton("✅ Принимать", callback_data="requests:end:yes")
).add(
    InlineKeyboardButton("🚫 Не принимать", callback_data="requests:end:no")
)

delete_markup = InlineKeyboardMarkup()
delete_markup.add(
    InlineKeyboardButton("❌ Удалить", callback_data="requests:confirm:delete"),
).add(
    InlineKeyboardButton("◀️ Не удалять", callback_data="admin:cancel")
)


async def paginate_groups_markup(db: AsyncSession, page: int):
    count_requests, requests = await get_requests(db)
    keyboard = InlineKeyboardMarkup()
    total_page = int(count_requests/10)
    buttons = paginate(requests, page=page, limit=10)
    data = "adm:rq:pg:"

    for request in buttons:
        keyboard.add(InlineKeyboardButton(f"🗃 ID: {request.channel_id}",
                                          callback_data=f"adm:req:{request.channel_id}"))

    if page + 1 <= total_page:
        keyboard.add(InlineKeyboardButton("▶️ Дальше", callback_data=data + f"{page+1}"))
    if page - 1 >= 0:
        keyboard.add(InlineKeyboardButton("◀️ Назад", callback_data=data + f"{page-1}"))

    keyboard.add(
        InlineKeyboardButton(f"👀 {page + 1}/{total_page+1}", callback_data="none"),
        InlineKeyboardButton("◀️ Назад в меню", callback_data="admin:groups_requests"))

    return keyboard


def request_markup(channel_id: int, accept: bool):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton("👁 Посмотреть пост", callback_data=f"request:view_post:{channel_id}")
    ).add(
        InlineKeyboardButton("🔧 Изменить пост", callback_data=f"request:change_post:{channel_id}")
    )

    accept_button = InlineKeyboardButton("#️⃣ Выключить принятия заявок", callback_data=f"request:approve:off:{channel_id}") \
        if accept is True else \
        InlineKeyboardButton("⏺ Включить принятия заявок", callback_data=f"request:approve:on:{channel_id}")

    keyboard.add(accept_button)
    keyboard.add(InlineKeyboardButton("◀️ Назад", callback_data="adm:rq:pg:0"))

    return keyboard


def buttons_markup(buy_status, hide_status):
    keyboard = InlineKeyboardMarkup()

    buy_button = InlineKeyboardButton("⏺ Включить кнопку рекламы", callback_data="admin:button_buy:on") if buy_status is False \
        else InlineKeyboardButton("#️⃣ Выключить кнопку рекламы", callback_data="admin:button_buy:off")
    hide_button = InlineKeyboardButton("⏺ Включить кнопку скрытия", callback_data="admin:button_hide:on") if hide_status is False \
        else InlineKeyboardButton("#️⃣ Выключить кнопку скрытия", callback_data="admin:button_hide:off")

    keyboard.add(InlineKeyboardButton("🔗 Сменить ссылку", callback_data="admin:button_url:change"))
    keyboard.add(buy_button).add(hide_button)
    keyboard.add(
        InlineKeyboardButton("◀️ Назад", callback_data="admin:settings")
    )

    return keyboard
