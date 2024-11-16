from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.dispatcher import FSMContext

from tg_bot.loader import dp
from tg_bot.states.admin import RefUrl
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.keyboards.admin.inline.ref import ref_markup
from tg_bot.keyboards.admin.inline.default import cancel_markup
from tg_bot.db_api.crud.referral import delete_referral_url, get_referral_url


@dp.callback_query_handler(IsAdmin(), text="ref_urls:delete")
async def ref_url_delete_handler(call: CallbackQuery):
    await call.message.edit_text("<b>🔗 Введите название для реферальной ссылки</b>",
                                 reply_markup=cancel_markup)
    await RefUrl.delete.set()


@dp.message_handler(IsAdmin(), state=RefUrl.delete)
async def delete_ref_url_handler(message: Message, state: FSMContext,
                                 session: AsyncSession):
    ref_url = await get_referral_url(session, message.text)

    if ref_url is None:
        await message.answer("<b>🚫 Данная ссылка не существует!</b>",
                             reply_markup=cancel_markup)
    else:
        await state.finish()
        await delete_referral_url(session, message.text)
        await message.answer("<b>ℹ️ Реферальная ссылка удалена!</b>",
                             reply_markup=ref_markup)
