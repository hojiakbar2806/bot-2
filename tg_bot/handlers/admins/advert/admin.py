from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from tg_bot.loader import dp
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.keyboards.admin.inline.ref import ref_markup
from tg_bot.keyboards.admin.inline.required_sub import required_markup
from tg_bot.keyboards.admin.inline.default import adv_markup, mailing_markup


@dp.message_handler(IsAdmin(), commands="ad", state="*")
@dp.message_handler(IsAdmin(), text="📊 Реклама", state="*")
async def adv_handler(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("<u>📊 Реклама</u>", reply_markup=adv_markup)


@dp.callback_query_handler(IsAdmin(), text="adv:mailing")
async def mailing_handler(call: CallbackQuery):
    await call.message.edit_text("<b>📧 Рассылка</b>", reply_markup=mailing_markup)


@dp.callback_query_handler(IsAdmin(), text="adv:ref_urls")
async def ref_handler(call: CallbackQuery):
    await call.message.edit_text("<b>🔗 Реферальные ссылки</b>",
                                 reply_markup=ref_markup)


@dp.callback_query_handler(IsAdmin(), text="adv:required_subs")
async def required_subs_handler(call: CallbackQuery):
    await call.message.edit_text("<b>🧑‍💻 Обязательная подписка</b>",
                                 reply_markup=required_markup)


@dp.callback_query_handler(IsAdmin(), text="admin:mailing_md", state="*")
async def adv_handler(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("<u>📊 Реклама</u>", reply_markup=adv_markup)
