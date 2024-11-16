from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.dispatcher import FSMContext

from tg_bot.loader import dp
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.utils.texts import get_stats_info
from tg_bot.keyboards.admin.reply import admin_markup


@dp.message_handler(IsAdmin(), commands="admin", state="*")
async def command_start(message: Message, session: AsyncSession, state: FSMContext):
    await state.finish()
    text = await get_stats_info(session)
    await message.answer(text, reply_markup=admin_markup)


@dp.callback_query_handler(IsAdmin(), text="admin:cancel", state="*")
async def cancel_handler(call: CallbackQuery, state: FSMContext,
                         session: AsyncSession):
    await state.finish()
    text = await get_stats_info(session)
    await call.message.delete()
    await call.message.answer(text, reply_markup=admin_markup)
