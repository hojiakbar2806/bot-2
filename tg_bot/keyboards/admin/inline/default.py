from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


cancel_markup = InlineKeyboardMarkup()
cancel_markup.add(
    InlineKeyboardButton("🙅🏻‍♂️ Отменить", callback_data="admin:cancel")
)

adv_markup = InlineKeyboardMarkup()
adv_markup.add(
    InlineKeyboardButton("📧 Рассылка", callback_data="adv:mailing")
).add(
    InlineKeyboardButton("🔗 Реферальные ссылки", callback_data="adv:ref_urls")
).add(
    InlineKeyboardButton("🧑‍💻 Обязательная подписка", callback_data="adv:required_subs")
)

mailing_markup = InlineKeyboardMarkup()
mailing_markup.add(
    InlineKeyboardButton("📧 Создать рассылку", callback_data="admin:ml:create")
).add(
    InlineKeyboardButton("🧾 Управление рассылками", callback_data="admin:ml:list")
).add(
    InlineKeyboardButton("◀️ Назад", callback_data="admin:mailing_md")
)

choose_markup = InlineKeyboardMarkup()
choose_markup.add(
    InlineKeyboardButton("🫂 Пользователи", callback_data="mailing_choose:users")
).add(
    InlineKeyboardButton("◀️ Назад", callback_data="admin:mailing_md")
)


settings_markup = InlineKeyboardMarkup()
settings_markup.add(
    InlineKeyboardButton("👮‍♂️ Админ Состав", callback_data="admin:admins")
).add(
    InlineKeyboardButton("🗄 Заявки в каналах", callback_data="admin:groups_requests")
).add(
    InlineKeyboardButton("🤖 BotStat", callback_data="admin:botstat")
).add(
    InlineKeyboardButton("🗂 Бэкап", callback_data="admin:backup")
).add(
    InlineKeyboardButton("↪️ Кнопки", callback_data="admin:buttons")
)

logs_markup = InlineKeyboardMarkup()
logs_markup.add(
    InlineKeyboardButton("🗒 Выгрузить юзеров | .sql", callback_data="owner:backup:users:sql")
).add(
    InlineKeyboardButton("🗒 Выгрузить юзеров | .txt", callback_data="owner:backup:users:txt")
).add(
    InlineKeyboardButton("🗒 Выгрузить конфиги и логи", callback_data="owner:backup:configs")
).add(
    InlineKeyboardButton("🗒 Выгрузить файлы", callback_data="owner:backup:files")
)
