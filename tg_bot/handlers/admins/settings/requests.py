from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.loader import dp, storage
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.keyboards.admin.reply import admin_markup
from tg_bot.keyboards.admin.inline.default import cancel_markup
from tg_bot.db_api.crud.requests import add_request, select_request, \
    delete_request, change_accept_request, change_post_request
from tg_bot.states.admin import RequestsAdd, RequestsDelete, RequestsChangePost
from tg_bot.keyboards.admin.inline.settings import requests_markup, continue_markup, \
    accept_markup, delete_markup, paginate_groups_markup, request_markup


@dp.callback_query_handler(IsAdmin(), text="admin:groups_requests")
async def admins_handler(call: CallbackQuery):
    await call.message.edit_text("<u>🗄 Заявки в каналах</u>", reply_markup=requests_markup)


@dp.callback_query_handler(IsAdmin(), text="admin:requests:active")
async def groups_active_handler(call: CallbackQuery, session: AsyncSession):
    await call.message.edit_text("<b>🗄 Активные каналы в принятия заявок</b>",
                                 reply_markup=await paginate_groups_markup(session, 0))


@dp.callback_query_handler(IsAdmin(),
                           text=["admin:requests:add", "admin:requests:delete"])
async def requests_add_handler(call: CallbackQuery):
    actions = {
        "admin:requests:add": [
            "<b>🗄 Введите ID канала для приема заявок: </b>",
            RequestsAdd.channel_id],
        "admin:requests:delete": [
            "<b>🗄 Введите ID канала для удаления с приема заявок: </b>",
            RequestsDelete.channel_id]
    }
    await call.message.edit_text(actions[call.data][0],
                                 reply_markup=cancel_markup)
    await actions[call.data][1].set()


@dp.message_handler(IsAdmin(), state=RequestsAdd.channel_id)
async def requests_channel_id_handler(message: Message, state: FSMContext,
                                      session: AsyncSession):
    try:
        channel_id = int(message.text)
    except ValueError:
        return await message.answer("<b>🚫 Введите ID канала: </b>")

    if await select_request(session, channel_id) is not None:
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
            await message.answer("<b>👁 Введите пост, который отправляется при приеме заявке: </b>\n"
                                 "🗒 Если не нужно, введите: <code>Не добавлять</code>\n\n"
                                 "<i>ℹ️ Принимается любой текст с разметкой, кнопками, видео, картинками и т.д</i>",
                                 reply_markup=cancel_markup)
            await RequestsAdd.post.set()
        else:
            await message.answer("<b>ℹ️ Бот не администратор в группе!\n"
                                 "➡️ Продолжить?</b>",
                                 reply_markup=continue_markup)


@dp.callback_query_handler(IsAdmin(), state=RequestsAdd.channel_id,
                           text="requests:continue")
async def requests_continue_handler(call: CallbackQuery):
    await call.message.edit_text(
        "<b>👁 Введите пост, который отправляется при приеме заявке: </b>\n"
        "🗒 Если не нужно, введите: <code>Не добавлять</code>\n\n"
        "<i>ℹ️ Принимается любой текст с разметкой, кнопками, видео, картинками и т.д</i>",
        reply_markup=cancel_markup)
    await RequestsAdd.post.set()


@dp.callback_query_handler(IsAdmin(), state=RequestsAdd.channel_id,
                           text="requests:refresh")
async def requests_refresh_handler(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.edit_text("<b>🗄 Введите ID канала для приема заявок: </b>",
                                 reply_markup=cancel_markup)
    await RequestsAdd.channel_id.set()


@dp.message_handler(IsAdmin(), state=RequestsAdd.post, content_types=ContentType.ANY)
async def requests_post_handler(message: Message, state: FSMContext):
    if message.text == "Не добавлять":
        await state.update_data(post=-1, chat_id=-1, reply_markup={})
    else:
        await state.update_data(post=message.message_id,
                                chat_id=message.chat.id,
                                reply_markup=message.reply_markup.as_json())

    await message.answer("<b>🫂 Принимать заявки для этого канала?</b>",
                         reply_markup=accept_markup)
    await RequestsAdd.accept.set()


@dp.callback_query_handler(IsAdmin(), state=RequestsAdd.accept)
async def requests_end_handler(call: CallbackQuery, state: FSMContext,
                               session: AsyncSession):
    data = await state.get_data()
    accept = True if call.data[len("requests:end:"):] == "yes" else False
    accept_text = "Принимаются" if accept is True else "Не принимаются"

    await state.finish()
    await add_request(session, data["channel_id"], data["post"],
                      data["chat_id"],
                      None if not data["reply_markup"] else data["reply_markup"],
                      accept)
    await call.message.edit_text("<b>🗄 Новый канал в принятии заявок был добавлен!</b>\n\n"
                                 f"🆔 ID Канала: <code>{data['channel_id']}</code>\n"
                                 f"🫂 Заявки <code>{accept_text}</code>\n\n"
                                 f"👁 Пост: ",
                                 reply_markup=requests_markup)

    if data["post"] != -1:
        await call.bot.copy_message(call.message.chat.id,
                                    call.message.chat.id,
                                    data["post"],
                                    reply_markup=data["reply_markup"])


@dp.message_handler(IsAdmin(), state=RequestsDelete.channel_id)
async def delete_request_handler(message: Message, state: FSMContext,
                                 session: AsyncSession):
    _request = await select_request(session, int(message.text))

    if _request is not None:
        await state.update_data(channel_id=message.text)
        await message.answer(f"<b>🗄 Вы точно хотите удалить канал</b> "
                             f"🆔 <code>{message.text}</code>\n",
                             reply_markup=delete_markup)
    else:
        await message.answer("<b>🚫 Канал на принятие заявки с таким ID не найден!</b>\n"
                             "ℹ️ Повторите попытку: ",
                             reply_markup=cancel_markup)


@dp.callback_query_handler(IsAdmin(), text="requests:confirm:delete",
                           state=RequestsDelete.channel_id)
async def confirm_request_handler(call: CallbackQuery, state: FSMContext,
                                  session: AsyncSession):
    data = await state.get_data()

    await state.finish()
    await delete_request(session, int(data["channel_id"]))
    await call.message.answer("<b>🗄 Канал был удален с принятия заявок!</b>",
                              reply_markup=admin_markup)


@dp.callback_query_handler(IsAdmin(), text_startswith="adm:rq:pg:")
async def paginate_request_handler(call: CallbackQuery, session: AsyncSession):
    page: int = int(call.data[len("adm:rq:pg:"):])

    await call.message.edit_text("<b>🗄 Активные каналы в принятия заявок</b>",
                                 reply_markup=await paginate_groups_markup(session, page))


@dp.callback_query_handler(IsAdmin(), text_startswith="adm:req:")
async def active_channel_handler(call: CallbackQuery, session: AsyncSession):
    channel_id: int = int(call.data[len("adm:req:"):])
    request = await select_request(session, channel_id)
    checked_text = "Да" if request.accept_request is True else 'Нет'

    text = "<b>🗄 Канал в принятие заявок: </b>\n\n" \
           f"<b>🆔 ID:</b> <code>{channel_id}</code>\n" \
           f"<b>🫂 Принимаются:</b> <code>{checked_text}</code>"

    await call.message.edit_text(text,
                                 reply_markup=request_markup(channel_id,
                                                             request.accept_request))


@dp.callback_query_handler(IsAdmin(), text_startswith="request:view_post:")
async def view_post_handler(call: CallbackQuery, session: AsyncSession):
    channel_id: int = int(call.data[len("request:view_post:"):])

    request = await select_request(session, channel_id)

    if request.message_id != -1:
        await dp.bot.copy_message(call.message.chat.id,
                                  request.message_chat_id,
                                  request.message_id,
                                  reply_markup=request.reply_markup)
    else:
        await call.answer("🚫 Данный канал не имеет поста!")


@dp.callback_query_handler(IsAdmin(), text_startswith="request:approve:")
async def view_post_handler(call: CallbackQuery, session: AsyncSession):
    action, channel_id = call.data[len("request:approve:"):].split(":")

    new_value: bool = True if action == "on" else False
    text = "*️⃣ Принятие заявок включено" if action == "on" \
        else "❌ Принятие заявок выключено"

    await change_accept_request(session, int(channel_id), new_value)
    await call.message.edit_reply_markup(reply_markup=request_markup(channel_id, new_value))
    await call.answer(text)


@dp.callback_query_handler(IsAdmin(), text_startswith="request:change_post:")
async def change_post_handler(call: CallbackQuery):
    channel_id: int = int(call.data[len("request:change_post:"):])

    await call.message.answer("<b>👁 Отправьте новый пост: </b>\n\n"
                              "<i>ℹ️ Принимается разметка, кнопки, видео, картинки и т.д</i>",
                              reply_markup=cancel_markup)
    await RequestsChangePost.post.set()
    await FSMContext(storage, call.message.chat.id, call.from_user.id)\
        .update_data(channel_id=channel_id)


@dp.message_handler(IsAdmin(), state=RequestsChangePost.post,
                    content_types=ContentType.ANY)
async def new_post_handler(message: Message, state: FSMContext,
                           session: AsyncSession):
    data = await state.get_data()
    reply_markup = None if not message.reply_markup else message.reply_markup

    await state.finish()
    await change_post_request(session, data["channel_id"], message.chat.id,
                              message.message_id, reply_markup)
    await message.answer("👁 Новый пост был поставлен!")
