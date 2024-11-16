from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


default_markup = InlineKeyboardMarkup()
default_markup.add(
    InlineKeyboardButton("🔎 Проверить юзеров | BotStat", callback_data="validate:botstat")).add(
    InlineKeyboardButton("☠️ Удалить мертвых | .txt", callback_data="db:delete_dead")).add(
    InlineKeyboardButton("🔍 Найти пользователя", callback_data="db:search_user"))


def search_user_markup(user_id, user_ban):
    keyboard = InlineKeyboardMarkup()

    button = \
        InlineKeyboardButton("⏺ Разблокировать", callback_data=f"unban:{user_id}") \
        if user_ban is True else \
        InlineKeyboardButton("#️⃣ Заблокировать",
                             callback_data=f"ban:{user_id}")

    keyboard.add(button)
    keyboard.add(
        InlineKeyboardButton("✉️ Отправить сообщение",
                             callback_data=f"send_message:{user_id}")
    )

    return keyboard
