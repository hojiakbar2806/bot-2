from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from tg_bot.loader import dp
from tg_bot.filters.is_number import IsNumber
from tg_bot.db_api.crud.bill import register_bill, select_bill
from tg_bot.utils.logger import logger
from tg_bot.db_api.crud.users import change_user_balance, change_user_premium
from tg_bot.keyboards.users.inline import qiwi_form_markup, cancel_markup
from tg_bot.states.users import DepositQiwiApi
from tg_bot.utils.settings import parse_settings
from tg_bot.services import notify_payment_to_owner, notify_error_to_owner
from tg_bot.db_api.crud.deposits import register_deposit
from tg_bot.services.payments.qiwi_pay import create_payment_url, payment_history_last


@dp.callback_query_handler(text_startswith="deposit:qiwi_api:")
async def process_qiwi_handler(call: CallbackQuery, session: AsyncSession, state: FSMContext):
    period = call.data[len("deposit:qiwi_p2p:"):]
    amount = parse_settings()["premium"][period]
    payments_settings = parse_settings()['payments']['qiwi_api']

    bill_id: int = await register_bill(session, call.from_user.id, amount)
    comment: str = f"{bill_id}_{call.from_user.id}"
    requisite_text, url = create_payment_url(call, payments_settings, comment, amount)

    await state.finish()
    await call.message.answer(
        "<b>Счет создан!</b>\n"
        f"Переведите <code>{amount}</code> ₽ на следующие реквизиты: \n" +
        requisite_text +
        f"Комментарий: <code>{comment}</code>\n\n"
        f"<i>После оплаты нажмите кнопку </i>",
        reply_markup=qiwi_form_markup(url, bill_id)
    )


@dp.callback_query_handler(text_startswith="qiwi_api:check:")
async def check_qiwi_paid_handler(call: CallbackQuery, session: AsyncSession):
    bill_id: int = call.data[len("qiwi_api:check:"):]
    comment: str = f"{bill_id}_{call.from_user.id}"

    try:
        payments_history = await payment_history_last(
            call.bot.config.payments.qiwi.qiwi_api.phone,
            call.bot.config.payments.qiwi.qiwi_api.token
        )
    except Exception as e:
        await notify_error_to_owner(dp, "Qiwi API", e)
        return await call.answer("Произошла ошибка, попробуйте еще раз!")

    for payment in payments_history['data']:
        if payment["comment"] == comment:
            if payment['sum']['currency'] == 643:
                db_bill = await select_bill(session, bill_id)
                if db_bill is not None:
                    return await call.message.edit_text("Вы оплатили счёт не в рублях, счет был отменен.")
                else:
                    await register_bill(session, call.from_user.id, payment['sum']['amount'])
                    amount = int(payment['sum']['amount'])
                    amounts = parse_settings()["premium"]

                    delta = timedelta(days=1) if amount == amounts["day"] else (
                        timedelta(days=7) if amount == amounts["week"] else (
                            timedelta(days=30) if amount == amounts["month"] else timedelta(days=365)))
                    new_date = datetime.now() + delta

                    await change_user_premium(session, call.from_user.id, new_date)

                    logger.info(
                        f"QIWI API | uid: {call.from_user.id} | Комментарий: {comment} | Сумма: {payment['sum']['amount']}"
                    )
                    await notify_payment_to_owner(dp, "Qiwi API", payment["sum"]["amount"], call.from_user.id)
                    await register_deposit(session, call.from_user.id, payment["sum"]["amount"], "qiwi_api")
                    return await call.message.edit_text("✅ Оплата успешно пройдена!\n"
                                                        f"Премиум будет работать до {new_date.strftime('%d.%m.%Y %H:%M')}")
            else:
                return await call.message.edit_text("Вы оплатили счёт не в рублях, счет был отменен.")
