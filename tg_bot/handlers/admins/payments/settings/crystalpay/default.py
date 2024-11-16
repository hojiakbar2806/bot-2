from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from tg_bot.loader import dp
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.keyboards.admin.inline.payments import crystal_pay_settings_markup, payment_system_markup
from tg_bot.utils.settings import parse_settings
from tg_bot.config import change_env
from tg_bot.keyboards.admin.inline.default import cancel_markup
from tg_bot.states.admin import ChangeCPName


@dp.callback_query_handler(IsAdmin(), text="payments:settings:crystal_pay")
async def payments_settings(call: CallbackQuery):
    settings = parse_settings()['payments']['crystal_pay']
    await call.message.edit_text("<u>💳 Crystal Pay</u>",
                                 reply_markup=crystal_pay_settings_markup(settings['active']))


@dp.callback_query_handler(IsAdmin(), text_startswith="payments:change_name:crystal_pay")
async def change_token_handler(call: CallbackQuery):
    await call.message.edit_text(f"<b>Введите новое название кассы для Crystal Pay: </b>",
                                 reply_markup=cancel_markup)
    await ChangeCPName.new_name.set()


@dp.message_handler(IsAdmin(), state=ChangeCPName.new_name)
async def set_new_nick_handler(message: Message, state: FSMContext):
    await state.finish()
    change_env("CRYSTALPAY_NAME", message.text)
    message.bot.config.payments.crystalpay.name = message.text
    await message.answer(f"<b>Новое название кассы для Crystal Pay было установлено</b>",
                         reply_markup=payment_system_markup)
