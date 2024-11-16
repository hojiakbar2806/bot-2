from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from tg_bot.loader import dp
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.keyboards.admin.inline.payments import qiwi_api_settings_markup, payment_system_markup
from tg_bot.keyboards.admin.inline.default import cancel_markup
from tg_bot.services.payments.qiwi_pay import check_qiwi_token
from tg_bot.states.admin import ChangeNumber, ChangeNickname
from tg_bot.config import change_env
from tg_bot.utils.settings import change_settings, parse_settings


@dp.callback_query_handler(IsAdmin(), text="payments:settings:qiwi_api")
async def payments_settings(call: CallbackQuery):
    settings = parse_settings()['payments']['qiwi_api']
    await call.message.edit_text("<u>💳 QIWI API</u>\n",
                                 reply_markup=qiwi_api_settings_markup(
                                     settings['active'], settings['nickname']))


@dp.callback_query_handler(IsAdmin(), text="payments:check_ban:qiwi_api")
async def check_qiwi_ban_handler(call: CallbackQuery):
    blocked = await check_qiwi_token(call.bot.config.payments.qiwi.qiwi_api.token)
    if blocked is not None:
        text = "<b>Кошелек не заблокирован!</b>" if blocked is False else "<b>Кошелек заблокирован</b>"
    else:
        text = "<b>Проверьте токен!</b>"

    await call.message.edit_text(text, reply_markup=call.message.reply_markup)


@dp.callback_query_handler(IsAdmin(), text_startswith="payments:change_number:qiwi_api")
async def change_token_handler(call: CallbackQuery):
    await call.message.edit_text(f"<b>Введите новый номер для QIWI API: </b>",
                                 reply_markup=cancel_markup)
    await ChangeNumber.number.set()


@dp.message_handler(IsAdmin(), state=ChangeNumber.number)
async def set_new_token_handler(message: Message, state: FSMContext):
    await state.finish()
    change_env("QIWI_API_PHONE", message.text)
    message.bot.config.payments.qiwi.qiwi_api.phone = message.text
    await message.answer(f"<b>Новый номер для QIWI API был установлен</b>",
                         reply_markup=payment_system_markup)


@dp.callback_query_handler(IsAdmin(), text_startswith=["payments:nick:disable:",
                                                       "payments:nick:enable:"])
async def enable_action_handler(call: CallbackQuery):
    action, service = call.data[len("payments:nick:"):].split(":")
    action = True if action == "enable" else False
    change_settings("payments", action, "qiwi_api", "nickname")
    settings = parse_settings()['payments']['qiwi_api']
    print(settings)

    text = "Перевод по нику включен!" if action is True else "Перевод по нику выключен!"
    markup = {
        "qiwi_api": qiwi_api_settings_markup(settings['active'], action)
    }

    await call.answer(text)
    await call.message.edit_reply_markup(markup[service])


@dp.callback_query_handler(IsAdmin(), text_startswith="payments:change_nick:qiwi_api")
async def change_token_handler(call: CallbackQuery):
    await call.message.edit_text(f"<b>Введите новый никнейм для QIWI API: </b>",
                                 reply_markup=cancel_markup)
    await ChangeNickname.nickname.set()


@dp.message_handler(IsAdmin(), state=ChangeNickname.nickname)
async def set_new_nick_handler(message: Message, state: FSMContext):
    await state.finish()
    change_env("QIWI_API_NICKNAME", message.text)
    message.bot.config.payments.qiwi.qiwi_api.nick = message.text
    await message.answer(f"<b>Новый ник для QIWI API был установлен</b>",
                         reply_markup=payment_system_markup)
