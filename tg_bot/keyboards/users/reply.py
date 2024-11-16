from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    KeyboardButton


menu_markup = ReplyKeyboardMarkup(resize_keyboard=True)
menu_markup.add(
    KeyboardButton("🔎 Поиск собеседника")
).add(
    KeyboardButton("👤 Профиль"),
    KeyboardButton("👑 Premium статус")
).add(
    KeyboardButton("📕 Правила")
)


cancel_search_markup = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_search_markup.add(
    KeyboardButton("🚫 Отменить поиск")
)

delete_markup = ReplyKeyboardRemove()
