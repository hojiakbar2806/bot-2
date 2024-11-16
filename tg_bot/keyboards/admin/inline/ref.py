from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ref_markup = InlineKeyboardMarkup()
ref_markup.add(
    InlineKeyboardButton("📈 Статистика", callback_data="ref_urls:stats")
).add(
    InlineKeyboardButton("*️⃣ Добавить", callback_data="ref_urls:create")
).add(
    InlineKeyboardButton("❌ Удалить", callback_data="ref_urls:delete")
).add(
    InlineKeyboardButton("◀️ Назад", callback_data="admin:mailing_md")
)
