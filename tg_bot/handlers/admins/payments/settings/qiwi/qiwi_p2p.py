from aiogram.types import CallbackQuery

from tg_bot.loader import dp
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.keyboards.admin.inline.payments import qiwi_p2p_settings_markup
from tg_bot.utils.settings import parse_settings


@dp.callback_query_handler(IsAdmin(), text="payments:settings:qiwi_p2p")
async def payments_settings(call: CallbackQuery):
    settings = parse_settings()['payments']['qiwi_p2p']
    await call.message.edit_text("<u>💳 QIWI P2P</u>",
                                 reply_markup=qiwi_p2p_settings_markup(settings['active']))
