import asyncio

from aiogram.types import Message, ChatType, ContentType
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.loader import dp, storage
from tg_bot.keyboards.users.inline import premium_markup, buy_premium_markup
from tg_bot.db_api.crud.users import get_user
from tg_bot.utils.settings import parse_settings
from tg_bot.db_api.crud.queue import get_user_in_queue, add_user_in_queue, select_user_from_queue, delete_user_from_queue
from tg_bot.db_api.crud.users import add_total_dialogs, add_total_messages
from tg_bot.db_api.crud.room import get_user_in_room, add_new_room, delete_room
from tg_bot.keyboards.users.reply import menu_markup, cancel_search_markup, delete_markup
from tg_bot.states.users import Chat


@dp.message_handler(commands="search", chat_type=ChatType.PRIVATE)
@dp.message_handler(text="🔎 Поиск собеседника", chat_type=ChatType.PRIVATE)
async def search_handler(message: Message, session: AsyncSession):
    queue = await get_user_in_queue(session, message.from_user.id)
    room = await get_user_in_room(session, message.from_user.id)
    text = "<i>Собеседник найден 🐵\n\n" \
           "/next — искать нового собеседника\n" \
           "/stop — закончить диалог\n" \
           "/sharelink - Поделиться своим ТГ</i>"
    user_db = await get_user(session, message.from_user.id)

    if queue is None and room is None:
        await add_user_in_queue(session, message.from_user.id, user_db.sex, user_db.opposite_sex, user_db.age)
        await message.answer("🔍 Ищу собеседника...", reply_markup=cancel_search_markup)

        while True:
            try:
                await asyncio.sleep(1)

                user_in_queue = await get_user_in_queue(session, message.from_user.id)

                if user_in_queue is not None:
                    connected_user = await select_user_from_queue(session, message.from_user.id, user_in_queue.opposite_sex)
                    print(connected_user)

                    if connected_user is not None:
                        connected_user_state = FSMContext(storage, connected_user.user_id, connected_user.user_id)

                        await delete_user_from_queue(session, message.from_user.id)
                        await delete_user_from_queue(session, connected_user.user_id)
                        await add_new_room(session, message.from_user.id, connected_user.user_id)

                        await connected_user_state.set_state(Chat.msg)
                        await connected_user_state.update_data(cust_id=message.from_user.id)

                        await Chat.msg.set()
                        await FSMContext(storage, message.from_user.id, message.from_user.id)\
                            .update_data(cust_id=connected_user.user_id)

                        await dp.bot.send_message(message.from_user.id, text, reply_markup=delete_markup)
                        await dp.bot.send_message(connected_user.user_id, text, reply_markup=delete_markup)

                        await add_total_dialogs(session, message.from_user.id)
                        await add_total_dialogs(session, connected_user.user_id)

                        break
                else:
                    break

            except Exception as e:
                print(e)
                break

    else:
        await message.answer("Вы уже в поиске/общаетесь!")


@dp.message_handler(text="🚫 Отменить поиск", chat_type=ChatType.PRIVATE)
async def stop_search_handler(message: Message, session: AsyncSession):
    await delete_user_from_queue(session, message.from_user.id)
    await message.answer("Поиск отменён 😿", reply_markup=menu_markup)


@dp.message_handler(commands="stop", state=Chat.msg, chat_type=ChatType.PRIVATE)
async def stop_handler(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    room = await get_user_in_room(session, message.from_user.id)
    text = "<i>Диалог остановлен 🤧\n"\
           "Отправьте /start, чтобы начать поиск</i>"

    await state.finish()
    await delete_room(session, room.room_id)
    await FSMContext(storage, data["cust_id"], data["cust_id"]).finish()
    await dp.bot.send_message(data["cust_id"], text, reply_markup=menu_markup)
    await message.answer(text, reply_markup=menu_markup)


@dp.message_handler(commands="next", state=Chat.msg, chat_type=ChatType.PRIVATE)
async def next_handler(message: Message, state: FSMContext, session: AsyncSession):
    await stop_handler(message, state, session)
    await search_handler(message, session)


@dp.message_handler(commands="sharelink", state=Chat.msg)
async def share_link_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    if message.from_user.username is not None:
        await dp.bot.send_message(
            data["cust_id"], f"📲 Собеседник поделился с вами своим контактом: {message.from_user.mention}")
        await message.answer("📲 Ваш контакт был отправлен собеседнику!")
    else:
        await message.answer("🚫 Вы не можете поделиться контактом, т.к у вас не установлен никнейм!")


@dp.message_handler(state=Chat.msg, content_types=ContentType.ANY)
async def chat_handler(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    await dp.bot.copy_message(data["cust_id"], message.chat.id, message.message_id)
    await add_total_messages(session, message.from_user.id)
