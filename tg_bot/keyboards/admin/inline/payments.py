from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


payments_markup = InlineKeyboardMarkup()
payments_markup.add(
    InlineKeyboardButton("⚙️ Настройки", callback_data="payments:settings")
).add(
    InlineKeyboardButton("📊 Статистика", callback_data="payments:stats")
)


payment_system_markup = InlineKeyboardMarkup()
payment_system_markup.add(
    InlineKeyboardButton("QIWI API", callback_data="payments:settings:qiwi_api"),
    InlineKeyboardButton("QIWI P2P", callback_data="payments:settings:qiwi_p2p")
).add(
    InlineKeyboardButton("Lolz", callback_data="payments:settings:lolz")
).add(
    InlineKeyboardButton("CrystalPay", callback_data="payments:settings:crystal_pay"),
).add(
    InlineKeyboardButton("◀️ Назад", callback_data="payments")
)


def default_markup(keyboard, active: bool, service):
    keyboard.add(InlineKeyboardButton("🔄 Сменить токен", callback_data=f"payments:change_token:{service}"))

    active_button = InlineKeyboardButton("#️⃣ Выключить прием платежей", callback_data=f"payments:disable:{service}") \
        if active is True else \
        InlineKeyboardButton("⏺ Включить прием платежей", callback_data=f"payments:enable:{service}")

    keyboard.add(InlineKeyboardButton("🔄 Проверить токен", callback_data=f"payments:check_token:{service}"))
    keyboard.add(active_button)
    keyboard.add(InlineKeyboardButton("🔂 Сменить минимальную сумму", callback_data=f"payments:change_min:{service}"))
    keyboard.add(InlineKeyboardButton("🔂 Сменить максимальную сумму", callback_data=f"payments:change_max:{service}"))
    keyboard.add(InlineKeyboardButton("◀️ Назад", callback_data="payments:settings"))

    return keyboard


def qiwi_api_settings_markup(active: bool = True, nickname: bool = False):
    keyboard = InlineKeyboardMarkup()

    nickname_button = InlineKeyboardButton("#️⃣ Выключить перевод по нику", callback_data="payments:nick:disable:qiwi_api") \
        if nickname is True else \
        InlineKeyboardButton("⏺ Включить перевод по нику", callback_data="payments:nick:enable:qiwi_api")

    keyboard.add(InlineKeyboardButton("🔄 Сменить номер", callback_data="payments:change_number:qiwi_api"))
    keyboard.add(InlineKeyboardButton("🔄 Сменить никнейм", callback_data="payments:change_nick:qiwi_api"))
    keyboard.add(nickname_button)
    keyboard = default_markup(keyboard, active, "qiwi_api")
    return keyboard


def qiwi_p2p_settings_markup(active: bool = True):
    keyboard = InlineKeyboardMarkup()
    keyboard = default_markup(keyboard, active, "qiwi_p2p")
    return keyboard


def lolz_settings_markup(active: bool, hold: bool):
    keyboard = InlineKeyboardMarkup()
    hold_button = InlineKeyboardButton("#️⃣ Выключить холд на день", callback_data="payments:hold:disable:lolz_pay") \
        if hold is True else \
        InlineKeyboardButton("⏺ Включить холд на день", callback_data="payments:hold:enable:lolz_pay")

    keyboard.add(hold_button)
    keyboard = default_markup(keyboard, active, "lolz_pay")
    return keyboard


def crystal_pay_settings_markup(active: bool):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔄 Сменить название кассы", callback_data="payments:change_name:crystal_pay"))
    keyboard = default_markup(keyboard, active, "crystal_pay")
    return keyboard
