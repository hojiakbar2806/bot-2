from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.dispatcher import FSMContext

from tg_bot.loader import dp
from tg_bot.utils.texts import get_bot_info
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.utils.functions import send_to_bot_safe
from tg_bot.keyboards.admin.inline.customers import default_markup


@dp.message_handler(IsAdmin(), commands="users", state="*")
@dp.message_handler(IsAdmin(), text="🫂 Пользователи", state="*")
async def command_start(message: Message, state: FSMContext):
    await state.finish()
    try:
        text = await get_bot_info()
    except:
        text = "<u>🫂 Пользователи</u>"
    await message.answer(text, reply_markup=default_markup)


@dp.callback_query_handler(IsAdmin(), text="validate:botstat")
async def validate_handler(call: CallbackQuery, session: AsyncSession):
    try:
        await send_to_bot_safe(session)
        await call.answer("✅ Проверка начата, вам придет новое сообщение")
    except:
        await call.answer("❌ Проверка не была начата, проверьте токен BotStat")
