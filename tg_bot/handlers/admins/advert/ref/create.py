from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.dispatcher import FSMContext

from tg_bot.loader import dp
from tg_bot.states.admin import RefUrl
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.keyboards.admin.inline.ref import ref_markup
from tg_bot.keyboards.admin.inline.default import cancel_markup
from tg_bot.db_api.crud.referral import add_referral_url, get_referral_url


@dp.callback_query_handler(IsAdmin(), text="ref_urls:create")
async def create_ml_handler(call: CallbackQuery):
    await call.message.edit_text("<b>🔗 Введите название для реферальной ссылки</b>",
                                 reply_markup=cancel_markup)
    await RefUrl.create.set()


@dp.message_handler(IsAdmin(), state=RefUrl.create)
async def create_ref_url_handler(message: Message, state: FSMContext,
                                 session: AsyncSession):
    ref_url = await get_referral_url(session, message.text)

    if ref_url is None:
        await state.finish()

        user_url = f"https://t.me/{message.bot.config.tgbot.username}?start=ad_{message.text}"
        chat_url = f"https://t.me/{message.bot.config.tgbot.username}?startgroup=ad_{message.text}"
        text = "<b>ℹ️ Реферальная ссылка создана!</b>\n" \
               f"<b>🔗 Ссылки: </b>\n" \
               f"{user_url}\n" \
               f"{chat_url}"

        await add_referral_url(session, message.text)
        await message.answer(text, reply_markup=ref_markup)

    else:
        await message.answer("<b>🚫 Данная ссылка уже существует!</b>",
                             reply_markup=cancel_markup)
