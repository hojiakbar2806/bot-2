from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from tg_bot.loader import dp
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.utils.texts import get_settings_info
from tg_bot.keyboards.admin.inline.default import settings_markup


@dp.message_handler(IsAdmin(), commands="settings", state="*")
@dp.message_handler(IsAdmin(), text="⚙️ Настройки", state="*")
async def command_start(message: Message, state: FSMContext):
    await state.finish()
    text = await get_settings_info()
    await message.answer(text, reply_markup=settings_markup)


@dp.callback_query_handler(IsAdmin(), text="admin:settings")
async def settings_handler(call: CallbackQuery):
    text = await get_settings_info()
    await call.message.edit_text(text, reply_markup=settings_markup)
