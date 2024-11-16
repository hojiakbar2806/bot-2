from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.dispatcher import FSMContext

from tg_bot.loader import dp, storage
from tg_bot.states.admin import RequiredSubURL
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.db_api.crud.required_subs import get_required_sub_by_sid,\
    change_sub_verify_by_sid, change_sub_url_by_sid, delete_sub_by_sid
from tg_bot.keyboards.admin.inline.default import cancel_markup
from tg_bot.keyboards.admin.inline.required_sub import paginate_subs_markup,\
    channel_markup, required_markup, confirm_delete_markup
from tg_bot.db_api.crud.users import select_list_users
from tg_bot.utils.functions import count_users, validate_block_bot


@dp.callback_query_handler(IsAdmin(), text="req_sub:stats")
async def create_ml_handler(call: CallbackQuery, session: AsyncSession):
    await call.message.edit_text("<b>🧑‍💻 Активные каналы в обязательной подписке</b>",
                                 reply_markup=await paginate_subs_markup(session, 0))


@dp.callback_query_handler(IsAdmin(), text_startswith="req_sub:pg:")
async def paginate_req_handler(call: CallbackQuery, session: AsyncSession):
    page: int = int(call.data[len("req_sub:pg:"):])

    await call.message.edit_text("<b>🧑‍💻 Активные каналы в обязательной подписке</b>",
                                 reply_markup=await paginate_subs_markup(session, page))


@dp.callback_query_handler(IsAdmin(), text_startswith="req:sub:")
async def active_req_handler(call: CallbackQuery, session: AsyncSession):
    channel_id: int = int(call.data[len("req:sub:"):])
    sub = await get_required_sub_by_sid(session, channel_id)
    checked_text = "Да" if sub.verify is True else 'Нет'

    _users = await select_list_users(session, sub.users_subbed)

    counts = count_users(_users)
    dead_users, alive_users = await validate_block_bot(dp, sub.users_subbed)

    text = "<b>🗄 Канал в принятие заявок: </b>\n\n" \
           f"<b>🆔 ID:</b> <code>{sub.channel_id}</code>\n" \
           f"<b>🔗 Ссылка</b>: {sub.channel_url}\n" \
           f"<b>🫂 Проверяется:</b> <code>{checked_text}</code>\n\n" \
           f"<b>↗️ Примерно перешло по ОП: </b><code>{len(sub.users_subbed)}</code>\n\n"\
           f"<b>😊 Живых:</b> <code>{len(alive_users)}</code>\n"\
           f"<b>☠️ Заблокировали:</b> <code>{len(dead_users)}</code>\n\n"\
           f"<b>➕ Прибавилось за Месяц:</b> <code>{counts[3]}</code>\n"\
           f"<b>➕ Прибавилось за Неделю:</b> <code>{counts[0]}</code>\n"\
           f"<b>➕ Прибавилось за День:</b> <code>{counts[1]}</code>\n"\
           f"<b>➕ Прибавилось за Час:</b> <code>{counts[2]}</code>"

    await call.message.edit_text(text, reply_markup=channel_markup(channel_id, sub.verify))


@dp.callback_query_handler(IsAdmin(), text_startswith="rq:verify:")
async def req_verify_handler(call: CallbackQuery, session: AsyncSession):
    action, channel_id = call.data[len("rq:verify:"):].split(":")

    new_value: bool = True if action == "on" else False
    text = "*️⃣ Проверка включена" if action == "on" \
        else "❌ Проверка выключена"
    call.data = f"req:sub:{channel_id}"

    await change_sub_verify_by_sid(session, int(channel_id), new_value)
    await active_req_handler(call, session)
    await call.answer(text)


@dp.callback_query_handler(IsAdmin(), text_startswith="rq:change_url:")
async def req_channel_url_handler(call: CallbackQuery):
    channel_id = call.data[len("rq:change_url:"):]

    await call.message.answer("<b>🔗 Введите новую ссылку на канал: </b>",
                              reply_markup=cancel_markup)
    await RequiredSubURL.new_url.set()
    await FSMContext(storage, call.message.chat.id, call.from_user.id)\
        .update_data(channel_id=channel_id)


@dp.message_handler(IsAdmin(), state=RequiredSubURL.new_url)
async def new_channel_url(message: Message, state: FSMContext,
                          session: AsyncSession):
    data = await state.get_data()

    await state.finish()
    await change_sub_url_by_sid(session, int(data["channel_id"]), message.text)
    await message.answer("<b>🔗 Ссылка изменена!</b>",
                         reply_markup=required_markup)


@dp.callback_query_handler(IsAdmin(), text_startswith="rq:delete:")
async def delete_sub_handler(call: CallbackQuery):
    channel_id = call.data[len("rq:delete:"):]

    await call.message.answer("<b>🚫 Вы уверены что хотите удалить канал с обязательной подписки?</b>",
                              reply_markup=confirm_delete_markup(channel_id))


@dp.callback_query_handler(IsAdmin(), text="req:cancel_delete")
async def delete_sub_handler(call: CallbackQuery):
    await call.message.delete()


@dp.callback_query_handler(IsAdmin(), text_startswith="req:delete:")
async def delete_sub_handler(call: CallbackQuery, session: AsyncSession):
    channel_id = call.data[len("req:delete:"):]

    await delete_sub_by_sid(session, int(channel_id))
    await call.message.edit_text("<b>❌ Канал был удален!</b>",
                                 reply_markup=required_markup)
