from aiogram.types import Message, CallbackQuery, ChatType
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from tg_bot.loader import dp
from tg_bot.filters.is_number import IsNumber
from tg_bot.db_api.crud.bill import register_bill
from tg_bot.utils.logger import logger
from tg_bot.db_api.crud.users import change_user_premium
from tg_bot.keyboards.users.inline import crystalpay_form_markup, cancel_markup
from tg_bot.utils.settings import parse_settings
from tg_bot.services import notify_payment_to_owner, notify_error_to_owner
from tg_bot.db_api.crud.deposits import register_deposit
from tg_bot.services.payments.crystal_pay import CrystalPay


@dp.callback_query_handler(text_startswith="deposit:crystal_pay:")
async def deposit_amount_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    period = call.data[len("deposit:crystal_pay:"):]
    amount = parse_settings()["premium"][period]

    await state.finish()

    bill_id: int = await register_bill(session, call.from_user.id, amount)
    comment: str = f"{bill_id}_{call.from_user.id}"

    try:
        async with CrystalPay(
            call.bot.config.payments.crystalpay.name,
            call.bot.config.payments.crystalpay.secret_key
        ) as api:
            payment = await api.create_invoice(amount, extra=comment)

        await call.message.answer("Перейдите по ссылке для оплаты!",
                                  reply_markup=crystalpay_form_markup(payment.url, payment.id))
    except Exception as e:
        await notify_error_to_owner(dp, "CrystalPay", e)
        return await call.message.answer("Произошла ошибка при выставлении счёта, попробуйте другой метод оплаты")


@dp.callback_query_handler(text_startswith="crystal_pay:check:", chat_type=ChatType.PRIVATE)
async def check_qiwi_bill(call: CallbackQuery, session: AsyncSession):
    payment_id: str = call.data[len("crystal_pay:check:"):]

    try:
        async with CrystalPay(
                call.bot.config.payments.crystalpay.name,
                call.bot.config.payments.crystalpay.secret_key
        ) as api:
            payment = api.construct_payment_by_id(payment_id)
    except Exception as e:
        await notify_error_to_owner(dp, "CrystalPay", e)
        return await call.answer("Произошла ошибка, попробуйте еще раз!")

    if await payment.check_paid() is True:
        amount = payment.amount if payment.amount is not None else await payment.get_amount()
        amount = float(amount)

        amounts = parse_settings()["premium"]

        delta = timedelta(days=1) if amount == amounts["day"] else (
            timedelta(days=7) if amount == amounts["week"] else (
                timedelta(days=30) if amount == amounts["month"] else timedelta(days=365)))
        new_date = datetime.now() + delta

        await change_user_premium(session, call.from_user.id, new_date)
        await call.message.edit_text("✅ Оплата успешно пройдена!\n"
                                     f"Премиум будет работать до {new_date.strftime('%d.%m.%Y %H:%M')}")

        await notify_payment_to_owner(dp, "CrystalPay", amount, call.from_user.id)
        await register_deposit(session, call.from_user.id, amount, "crystal_pay")
        logger.info(
            f"CrystalPay | uid: {call.from_user.id} | Комментарий: None | Сумма: {amount}"
        )
    else:
        await call.answer("Счёт не оплачен")


@dp.callback_query_handler(text_startswith="crystal_pay:cancel:")
async def cancel_qiwi_bill(call: CallbackQuery):
    await call.message.edit_text("❌ Вы отменили оплату!")
