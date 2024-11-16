from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.dispatcher import FSMContext

from tg_bot.loader import dp
from tg_bot.states.admin import RequiredSubAdd
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.keyboards.admin.inline.default import cancel_markup
from tg_bot.keyboards.admin.inline.required_sub import continue_markup, \
    verify_markup, required_markup
from tg_bot.db_api.crud.required_subs import get_required_sub, add_required_sub


@dp.callback_query_handler(IsAdmin(), text="req_sub:create")
async def create_ml_handler(call: CallbackQuery):
    await call.message.edit_text("<b>🧑‍💻 Введите ID канала: </b>\n"
                                 "<i>Для ботов используйте</i> <code>0</code>",
                                 reply_markup=cancel_markup)
    await RequiredSubAdd.channel_id.set()


@dp.message_handler(IsAdmin(), state=RequiredSubAdd.channel_id)
async def channel_id_handler(message: Message, state: FSMContext,
                             session: AsyncSession):
    try:
        channel_id = int(message.text)
    except ValueError:
        return await message.answer("<b>🚫 Введите ID канала: </b>")

    if await get_required_sub(session, channel_id) is not None:
        await message.answer("<b>🚫 Данный канал уже добавлен!\n"
                             "ℹ️ Попробуйте заново: </b>",
                             reply_markup=cancel_markup)
    else:
        await state.update_data(channel_id=channel_id)

        try:
            _in_channel = await dp.bot.get_chat_member(channel_id, message.bot.id)
        except:
            return await message.answer("<b>ℹ️ Бот не добавлен в группу!\n"
                                        "➡️ Продолжить?</b>",
                                        reply_markup=continue_markup)

        if _in_channel.status == "administrator":
            await message.answer("<b>🔗 Введите ссылку на канал: </b>",
                                 reply_markup=cancel_markup)
            await RequiredSubAdd.channel_url.set()
        else:
            await message.answer("<b>ℹ️ Бот не администратор в группе!\n"
                                 "➡️ Продолжить?</b>",
                                 reply_markup=continue_markup)


@dp.callback_query_handler(IsAdmin(), state=RequiredSubAdd.channel_id,
                           text="req_sub:continue")
async def requests_continue_handler(call: CallbackQuery):
    await call.message.edit_text("<b>🔗 Введите ссылку на канал: </b>", reply_markup=cancel_markup)
    await RequiredSubAdd.channel_url.set()


@dp.callback_query_handler(IsAdmin(), state=RequiredSubAdd.channel_id,
                           text="req_sub:refresh")
async def requests_refresh_handler(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("<b>🧑‍💻 Введите ID канала:</b>", reply_markup=cancel_markup)
    await RequiredSubAdd.channel_id.set()


@dp.message_handler(IsAdmin(), state=RequiredSubAdd.channel_url)
async def channel_url_handler(message: Message, state: FSMContext):
    await state.update_data(channel_url=message.text)
    await message.answer("<b>❔ Надо ли проверять подписку: </b>",
                         reply_markup=verify_markup)
    await RequiredSubAdd.verify.set()


@dp.callback_query_handler(IsAdmin(), text_startswith="req_sub:verify:",
                           state=RequiredSubAdd.verify)
async def verify_handler(call: CallbackQuery, state: FSMContext,
                         session: AsyncSession):
    verify = True if call.data[len("req_sub:verify:"):] == "yes" else False
    verify_text = 'Да'if verify is True else 'Нет'
    data = await state.get_data()

    await state.finish()
    await add_required_sub(session, data["channel_id"], data["channel_url"], verify)
    await call.message.edit_text("<b>🧑‍💻 Канал на подписку добавлен!</b>\n\n"
                                 f"<b>🆔 Айди канала: </b><code>{data['channel_id']}</code>\n"
                                 f"<b>🔗 Ссылка на канал: </b>{data['channel_url']}\n"
                                 f"<b>❔ Проверяется: </b><code>{verify_text}</code>",
                                 reply_markup=required_markup)
