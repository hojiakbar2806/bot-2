from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tg_bot.db_api.schemas.requiredsub import RequiredSub
from tg_bot.utils.settings import parse_settings


async def subscribe_markup(channels: list[RequiredSub]):
    keyboard = InlineKeyboardMarkup()

    for channel in channels:
        keyboard.add(InlineKeyboardButton("↗️ Подписаться", url=channel.channel_url))

    keyboard.add(InlineKeyboardButton("✅ Проверить подписку", callback_data="user:verify_required_subs"))
    return keyboard


async def payment_markup(period):
    keyboard = InlineKeyboardMarkup()
    settings = parse_settings()['payments']

    for payment_method in settings:
        if settings[payment_method]['active'] is True:
            keyboard.add(
                InlineKeyboardButton(
                    settings[payment_method]['real_name'],
                    callback_data=f"deposit:{payment_method}:{period}"
                )
            )

    return keyboard


def qiwi_form_markup(url, bill_id: int):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Перейти к оплате", url=url)
    ).add(
        InlineKeyboardButton("Проверить оплату", callback_data=f"qiwi_api:check:{bill_id}")
    )
    return keyboard


def qiwi_p2p_form_markup(url, bill_id):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton("💎 Перейти на сайт с оплатой", url=url))
    keyboard.add(InlineKeyboardButton("✅| Проверить оплату", callback_data=f"qiwi_p2p:check:{bill_id}"))
    keyboard.add(InlineKeyboardButton("❌| Отменить", callback_data=f"qiwi_p2p:cancel:{bill_id}"))
    return keyboard


def lolz_form_markup(url, comment):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton("💎 Перейти на сайт с оплатой", url=url))
    keyboard.add(InlineKeyboardButton("✅| Проверить оплату", callback_data=f"lolz_pay:check:{comment}"))
    keyboard.add(InlineKeyboardButton("❌| Отменить", callback_data=f"lolz_pay:cancel:{comment}"))
    return keyboard


def crystalpay_form_markup(url, comment):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton("💎 Перейти на сайт с оплатой", url=url))
    keyboard.add(InlineKeyboardButton("✅| Проверить оплату", callback_data=f"crystal_pay:check:{comment}"))
    keyboard.add(InlineKeyboardButton("❌| Отменить", callback_data=f"crystal_pay:cancel:{comment}"))
    return keyboard



cancel_markup = InlineKeyboardMarkup()
cancel_markup.add(
    InlineKeyboardButton("Отменить", callback_data="user:back_menu")
)

reg_sex_markup = InlineKeyboardMarkup()
reg_sex_markup.add(
    InlineKeyboardButton("🙎‍♂️ Парень", callback_data="man"),
    InlineKeyboardButton("🙍‍♀ Девушка️", callback_data="woman")
)


premium_markup = InlineKeyboardMarkup()
premium_markup.add(
    InlineKeyboardButton("Выбрать пол собеседника:", callback_data="choose:opposite_sex")
)


def buy_premium_markup(amount_day, amount_week, amount_month, amount_all):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(f"24 часа за {amount_day} ₽", callback_data="buy_premium:day"),
        InlineKeyboardButton(f"🔥 7 дней за {amount_week} ₽", callback_data="buy_premium:week"),
        InlineKeyboardButton(f"Месяц за {amount_month} ₽", callback_data="buy_premium:month"),
        InlineKeyboardButton(f"Навсегда за {amount_all} ₽", callback_data="buy_premium:all"),
    )
    return keyboard
