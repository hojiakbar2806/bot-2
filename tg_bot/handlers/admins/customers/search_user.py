from aiogram.types import Message, CallbackQuery, ContentType
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.dispatcher import FSMContext

from tg_bot.loader import dp, storage
from tg_bot.states.admin import SearchUser, UserMessage
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.keyboards.admin.inline.default import cancel_markup
from tg_bot.keyboards.admin.inline.customers import search_user_markup
from tg_bot.db_api.crud.users import get_user, get_user_by_username, change_ban_user
from tg_bot.db_api.crud.deposits import get_user_last_deposit
from tg_bot.utils.texts import get_service_name


@dp.callback_query_handler(IsAdmin(), text="db:search_user")
async def search_user_handler(call: CallbackQuery):
    await call.message.edit_text("<b>🔍 Введите @username или User ID: </b>",
                                 reply_markup=cancel_markup)
    await SearchUser.user.set()


@dp.message_handler(IsAdmin(), state=SearchUser.user)
async def search_handler(message: Message, session: AsyncSession,
                         state: FSMContext):
    await state.finish()

    if message.text.isdigit():
        user = await get_user(session, int(message.text))
    else:
        username = message.text[1:] if message.text[0] == "@" else message.text
        user = await get_user_by_username(session, username)

    if user:
        username = "Нет" if not user.username else user.username
        reg_date = user.registration_date.strftime('%d.%m.%Y %H:%M')
        user_banned = "Да" if user.ban is True else "Нет"
        user_registered = "Да" if user.registered is True else "Нет"
        last_deposit = await get_user_last_deposit(session, user.user_id)

        if last_deposit is not None:
            last_deposit_text = f"<code>{last_deposit.date.strftime('%d.%m.%Y')} " \
                                f"| {last_deposit.amount} " \
                                f"| {get_service_name(last_deposit.payment_system)}</code>"
        else:
            last_deposit_text = "<b>Не найдено</b>"

        try:
            await dp.bot.send_chat_action(user.user_id, "typing")
            user_blocked = "Нет"
        except:
            user_blocked = "☠️ Да"

        text = f"<b>ℹ️ Пользователь: </b><code>{user.user_id}</code>\n\n" \
               f"<b>👤 Полное имя: </b><code>{user.full_name}</code>\n" \
               f"<b>🚹 Юзернейм: </b><code>{username}</code>\n" \
               f"<b>📅 Дата регистрации в боте: </b><code>{reg_date}</code>\n" \
               f"<b>🚫 Забанен в боте: </b><code>{user_banned}</code>\n" \
               f"<b>🗣 ID кем приведен: </b><code>{user.referral_id}</code>\n" \
               f"<b>👁 Зарегистрирован в боте: </b><code>{user_registered}</code>\n" \
               f"<b>☠️ Забанил бота: </b><code>{user_blocked}</code>\n" \
               f"<b>Последнее пополнение: </b>{last_deposit_text}"

        await message.answer(text,
                             reply_markup=search_user_markup(user.user_id,
                                                             user.ban))
    else:
        await message.answer("🔍 Пользователь не найден!",
                             reply_markup=cancel_markup)


@dp.callback_query_handler(IsAdmin(), text_startswith="ban:")
async def ban_user_handler(call: CallbackQuery, session: AsyncSession):
    user_id: int = int(call.data[len("ban:"):])

    await change_ban_user(session, user_id, True)
    await call.message.edit_reply_markup(search_user_markup(user_id, True))


@dp.callback_query_handler(IsAdmin(), text_startswith="unban:")
async def ban_user_handler(call: CallbackQuery, session: AsyncSession):
    user_id: int = int(call.data[len("unban:"):])

    await change_ban_user(session, user_id, False)
    await call.message.edit_reply_markup(search_user_markup(user_id, False))


@dp.callback_query_handler(IsAdmin(), text_startswith="send_message:")
async def send_msg_handler(call: CallbackQuery):
    user_id: int = int(call.data[len("send_message:"):])

    await call.message.answer("<b>✉️ Отправьте сообщение для юзера: </b>",
                              reply_markup=cancel_markup)
    await UserMessage.msg.set()
    await FSMContext(storage, call.message.chat.id, call.from_user.id)\
        .update_data(user_id=user_id)


@dp.message_handler(IsAdmin(), state=UserMessage.msg, content_types=ContentType.ANY)
async def msg_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    await state.finish()
    m = await dp.bot.copy_message(
        data["user_id"],
        message.chat.id,
        message.message_id,
        reply_markup=message.reply_markup)
    await message.answer("<b>Сообщение было отправлено!</b>")
