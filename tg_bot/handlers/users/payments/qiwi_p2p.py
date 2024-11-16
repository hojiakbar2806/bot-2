import random

from aiogram.types import Message, ChatType, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.dispatcher import FSMContext
from datetime import datetime, timedelta
from pyqiwip2p import AioQiwiP2P

from tg_bot.loader import dp
from tg_bot.utils.logger import logger
from tg_bot.filters.is_number import IsNumber
from tg_bot.states.users import DepositQiwiP2P
from tg_bot.utils.settings import parse_settings
from tg_bot.services import notify_payment_to_owner, notify_error_to_owner
from tg_bot.db_api.crud.deposits import register_deposit
from tg_bot.db_api.crud.users import change_user_balance, change_user_premium
from tg_bot.keyboards.users.inline import cancel_markup, qiwi_p2p_form_markup
from tg_bot.utils.settings import parse_settings


@dp.callback_query_handler(text_startswith="deposit:qiwi_p2p:")
async def deposit_qiwi_handler(call: CallbackQuery):
    period = call.data[len("deposit:qiwi_p2p:"):]
    amount = parse_settings()["premium"][period]
    lifetime = 8
    comment = f'{call.from_user.id} payment'
    bill_id = random.randint(0, 9999999)

    try:
        async with AioQiwiP2P(call.bot.config.payments.qiwi.qiwi_p2p.token) as p2p:
            bill = await p2p.bill(bill_id=bill_id, amount=amount, comment=comment, lifetime=lifetime)

        await call.message.answer("Перейдите по ссылке для оплаты!",
                                  reply_markup=qiwi_p2p_form_markup(bill.pay_url, bill_id))
    except Exception as e:
        await notify_error_to_owner(dp, "Qiwi P2P", e)
        await call.message.answer("<b>Произошла ошибка при попытки выставление счета, попробуйте другой метод оплаты</b>")


@dp.callback_query_handler(text_startswith="qiwi_p2p:check:", chat_type=ChatType.PRIVATE)
async def check_qiwi_bill(call: CallbackQuery, session: AsyncSession):
    bill_id = call.data[len("qiwi_p2p:check:"):]

    try:
        async with AioQiwiP2P(call.bot.config.payments.qiwi.qiwi_p2p.token) as p2p:
            bill = await p2p.check(bill_id)
    except Exception as e:
        await notify_error_to_owner(dp, "Qiwi P2P", e)
        return await call.answer("Произошла ошибка, попробуйте еще раз!")

    if bill.status == "PAID":
        amount = float(bill.amount)
        amounts = parse_settings()["premium"]

        delta = timedelta(days=1) if amount == amounts["day"] else (
            timedelta(days=7) if amount == amounts["week"] else (
                timedelta(days=30) if amount == amounts["month"] else timedelta(days=365)))
        new_date = datetime.now() + delta

        await change_user_premium(session, call.from_user.id, new_date)
        await call.message.edit_text("✅ Оплата успешно пройдена!\n"
                                     f"Премиум будет работать до {new_date.strftime('%d.%m.%Y %H:%M')}")
        await p2p.reject(bill_id)
        await notify_payment_to_owner(dp, "Qiwi P2P", amount, call.from_user.id)
        await register_deposit(session, call.from_user.id, amount, "qiwi_p2p")
        logger.info(
            f"QIWI P2P | uid: {call.from_user.id} | Комментарий: None | Сумма: {amount}"
        )

    elif bill.status == "EXPIRED":
        await p2p.reject(bill_id)
        await call.message.edit_text("❌ Вы просрочили срок оплаты!\n"
                                     "Счет отменен")
    else:
        return


@dp.callback_query_handler(text_startswith="qiwi_p2p:cancel:", chat_type=ChatType.PRIVATE)
async def cancel_qiwi_bill(call: CallbackQuery):
    bill_id = call.data[len("qiwi_p2p:cancel:"):]
    async with AioQiwiP2P(call.bot.config.payments.qiwi.qiwi_p2p.token) as p2p:
        await p2p.reject(bill_id)

    await call.message.edit_text("❌ Вы отменили оплату!")
