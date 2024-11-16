from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.dispatcher import FSMContext

from tg_bot.loader import dp
from tg_bot.filters.admin_filter import IsOwner
from tg_bot.keyboards.admin.inline.payments import payments_markup
from tg_bot.db_api.crud.deposits import get_count_deposits, get_sum_amounts, get_deposits, get_max_amount
from tg_bot.utils.functions import count_payments


@dp.message_handler(IsOwner(), commands="payments", state="*")
@dp.message_handler(IsOwner(), text="💳 Платежки", state="*")
async def command_start(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("<u>💳 Платежки</u>", reply_markup=payments_markup)


@dp.callback_query_handler(IsOwner(), text="payments", state="*")
async def command_start(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("<u>💳 Платежки</u>", reply_markup=payments_markup)


@dp.callback_query_handler(IsOwner(), text="payments:stats", state="*")
async def payments_stats_handler(call: CallbackQuery, session: AsyncSession, state: FSMContext):
    total = await get_count_deposits(session)
    sum_amounts = await get_sum_amounts(session)
    deposits = await get_deposits(session)
    total_payments = count_payments(deposits)
    max_amount = await get_max_amount(session)

    text = f"<b>Статистика по платежам: </b>\n\n" \
           f"<b>Всего платежей: </b><code>{total}</code>\n" \
           f"<b>Платежей за неделю: </b><code>{total_payments[0]}</code>\n" \
           f"<b>Платежей за день: </b><code>{total_payments[1]}</code>\n" \
           f"<b>Платежей за час: </b><code>{total_payments[2]}</code>\n" \
           f"<b>Платежей за месяц: </b><code>{total_payments[3]}</code>\n\n" \
           f"<b>Сумма всех платежей: </b><code>{sum_amounts} ₽</code>\n\n" \
           f"<b>Самый большой платеж: </b><code>{max_amount} ₽</code>"

    await state.finish()
    await call.message.edit_text(text, reply_markup=payments_markup)
