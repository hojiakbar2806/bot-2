from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    KeyboardButton


admin_markup = ReplyKeyboardMarkup(resize_keyboard=True)
admin_markup.add(
    KeyboardButton("🫂 Пользователи"),
    KeyboardButton("💳 Платежки"),
).add(
    KeyboardButton("⚙️ Настройки"),
).add(
    KeyboardButton("📊 Реклама"),
    KeyboardButton("🗒 Логи")
)


cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancel_markup.add(
    KeyboardButton("🙅🏻‍♂️ Отменить")
)
