from aiogram.types import CallbackQuery

from tg_bot.loader import dp
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.keyboards.admin.inline.payments import lolz_settings_markup
from tg_bot.utils.settings import change_settings, parse_settings


@dp.callback_query_handler(IsAdmin(), text="payments:settings:lolz")
async def payments_settings(call: CallbackQuery):
    settings = parse_settings()['payments']['lolz_pay']
    await call.message.edit_text("<u>💳 Lolzteam</u>",
                                 reply_markup=lolz_settings_markup(settings['active'], settings['hold']))


@dp.callback_query_handler(IsAdmin(), text_startswith=["payments:hold:disable:", "payments:hold:enable:"])
async def enable_action_handler(call: CallbackQuery):
    action, service = call.data[len("payments:hold:"):].split(":")
    action = True if action == "enable" else False
    change_settings("payments", action, "lolz_pay", "hold")
    settings = parse_settings()['payments']['lolz_pay']

    text = "Холд включен!" if action is True else "Холд выключен!"
    markup = {
        "lolz_pay": lolz_settings_markup(settings['active'], action)
    }

    await call.answer(text)
    await call.message.edit_reply_markup(markup[service])
