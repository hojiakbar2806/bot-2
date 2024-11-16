import asyncio

from aiogram.types import Message, CallbackQuery, ChatType
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from tg_bot.loader import dp
from tg_bot.filters.is_number import IsNumber
from tg_bot.db_api.crud.bill import register_bill
from tg_bot.utils.logger import logger
from tg_bot.db_api.crud.users import change_user_premium
from tg_bot.keyboards.users.inline import lolz_form_markup, cancel_markup
from tg_bot.states.users import DepositLolz
from tg_bot.utils.settings import parse_settings
from tg_bot.services import notify_payment_to_owner, notify_error_to_owner
from tg_bot.db_api.crud.deposits import register_deposit
from tg_bot.services.payments.lolz_pay import Lolz


@dp.callback_query_handler(text_startswith="deposit:lolz_pay:")
async def deposit_amount_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    payments_settings = parse_settings()['payments']['lolz_pay']
    period = call.data[len("deposit:qiwi_p2p:"):]
    amount = parse_settings()["premium"][period]

    await state.finish()

    bill_id: int = await register_bill(session, call.from_user.id, amount)
    comment: str = f"{bill_id}_{call.from_user.id}"
    hold = 0 if payments_settings['hold'] is False else 1

    try:
        async with Lolz(call.bot.config.payments.lolz.api_key) as api:
            link = await api.get_link(amount, comment, hold)

        await call.message.answer("Перейдите по ссылке для оплаты!",
                             reply_markup=lolz_form_markup(link, comment))
    except Exception as e:
        await notify_error_to_owner(dp, "Lolzteam", e)
        return await call.message.answer("Произошла ошибка при выставлении счёта, попробуйте другой метод оплаты")


@dp.callback_query_handler(text_startswith="lolz_pay:check:", chat_type=ChatType.PRIVATE)
async def check_qiwi_bill(call: CallbackQuery, session: AsyncSession):
    comment = call.data[len("lolz_pay:check:"):]

    try:
        async with Lolz(call.bot.config.payments.lolz.api_key) as api:
            await asyncio.sleep(3)
            bill = await api.check_payment(comment)
    except Exception as e:
        await notify_error_to_owner(dp, "Lolzteam", e)
        return await call.answer("Произошла ошибка, попробуйте еще раз!")

    if bill is not False:
        if bill['is_finished'] == 1:
            amount = float(bill['incoming_sum'])
            amounts = parse_settings()["premium"]

            delta = timedelta(days=1) if amount == amounts["day"] else (
                timedelta(days=7) if amount == amounts["week"] else (
                    timedelta(days=30) if amount == amounts["month"] else timedelta(days=365)))
            new_date = datetime.now() + delta

            await change_user_premium(session, call.from_user.id, new_date)
            await call.message.edit_text("✅ Оплата успешно пройдена!\n"
                                         f"Премиум будет работать до {new_date.strftime('%d.%m.%Y %H:%M')}")
            await notify_payment_to_owner(dp, "Lolzteam", amount, call.from_user.id)
            await register_deposit(session, call.from_user.id, amount, "lolz_pay")
            logger.info(
                f"LolzTeam | uid: {call.from_user.id} | Комментарий: None | Сумма: {amount}"
            )
    else:
        await call.answer("Счёт не оплачен")


@dp.callback_query_handler(text_startswith="lolz_pay:cancel:")
async def cancel_qiwi_bill(call: CallbackQuery):
    await call.message.edit_text("❌ Вы отменили оплату!")
