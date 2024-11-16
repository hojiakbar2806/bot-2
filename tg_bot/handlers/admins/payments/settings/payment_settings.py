from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from tg_bot.loader import dp, storage
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.filters.is_number import IsNumber
from tg_bot.keyboards.admin.inline.payments import payment_system_markup, \
    qiwi_api_settings_markup, qiwi_p2p_settings_markup, lolz_settings_markup, crystal_pay_settings_markup
from tg_bot.keyboards.admin.inline.default import cancel_markup
from tg_bot.utils.settings import change_settings, parse_settings
from tg_bot.utils.texts import get_service_name, get_service_section
from tg_bot.states.admin import ChangePaymentAmount, ChangeToken
from tg_bot.config import change_env
from tg_bot.utils.functions import check_service_stable


@dp.callback_query_handler(IsAdmin(), text="payments:settings")
async def payments_settings(call: CallbackQuery):
    await call.message.edit_text("<u>💳 Платежки</u>\n"
                                 "<i>Выберите платежную систему: </i>",
                                 reply_markup=payment_system_markup)


@dp.callback_query_handler(IsAdmin(), text_startswith=["payments:disable:", "payments:enable:"])
async def enable_action_handler(call: CallbackQuery):
    action, service = call.data[len("payments:"):].split(":")
    action = True if action == "enable" else False
    change_settings("payments", action, service, "active")
    settings = parse_settings()['payments']

    text = "Платежная система включена!" if action is True else "Платежная система выключена!"
    markup = {
        "qiwi_api": qiwi_api_settings_markup(action, settings['qiwi_api']['nickname']),
        "qiwi_p2p": qiwi_p2p_settings_markup(settings['qiwi_p2p']['active']),
        "lolz_pay": lolz_settings_markup(settings['lolz_pay']['active'], settings['lolz_pay']['hold']),
        "crystal_pay": crystal_pay_settings_markup(settings["crystal_pay"]['active'])
    }

    await call.answer(text)
    await call.message.edit_reply_markup(markup[service])


@dp.callback_query_handler(IsAdmin(), text_startswith=["payments:change_min:", "payments:change_max:"])
async def change_amount_handler(call: CallbackQuery):
    action, service = call.data[len("payments:"):].split(":")

    await call.message.answer("<b>Введите новую сумму в рублях: </b>",
                              reply_markup=cancel_markup)
    await ChangePaymentAmount.new_amount.set()
    await FSMContext(storage, call.message.chat.id, call.from_user.id)\
        .update_data(action=action, service=service)


@dp.message_handler(IsNumber(), state=ChangePaymentAmount.new_amount)
async def change_amount_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    new_amount = float(message.text)
    section_name = "min" if data["action"] == "change_min" else "max"

    await state.finish()
    change_settings("payments", new_amount, data["service"], section_name)
    await message.answer("<b>Новая сумма поставлена!</b>",
                         reply_markup=payment_system_markup)


@dp.callback_query_handler(IsAdmin(), text_startswith="payments:change_token:")
async def change_token_handler(call: CallbackQuery):
    service = call.data[len("payments:change_token:"):]
    service_name = get_service_name(service)

    await call.message.edit_text(f"<b>Введите новый токен для {service_name}: </b>",
                                 reply_markup=cancel_markup)
    await ChangeToken.token.set()
    await FSMContext(storage, call.message.chat.id, call.from_user.id)\
        .update_data(service=service, service_name=service_name)


@dp.message_handler(IsAdmin(), state=ChangeToken.token)
async def set_new_token_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    service_section = get_service_section(data["service"])

    match data["service"]:
        case "qiwi_api":
            message.bot.config.payments.qiwi.qiwi_api.token = message.text
        case "qiwi_p2p":
            message.bot.config.payments.qiwi.qiwi_p2p.token = message.text
        case "crystal_pay":
            message.bot.config.payments.crystalpay.secret_key = message.text
        case "lolz_pay":
            message.bot.config.payments.lolz.api_key = message.text

    await state.finish()
    change_env(service_section, message.text)
    await message.answer(f"<b>Новый токен для {data['service_name']} был установлен</b>",
                         reply_markup=payment_system_markup)


@dp.callback_query_handler(IsAdmin(), text_startswith="payments:check_token:")
async def payments_settings(call: CallbackQuery):
    service = call.data[len("payments:check_token:"):]
    text = await check_service_stable(call, service)
    action = True if text == "<b>Токен работает</b>" else False

    change_settings("payments", action, service, "active")
    await call.message.edit_text(text, reply_markup=call.message.reply_markup)
