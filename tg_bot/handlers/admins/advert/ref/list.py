from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import CallbackQuery, Message

from tg_bot.loader import dp
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.keyboards.admin.inline.ref import ref_markup
from tg_bot.db_api.crud.referral import get_referral_urls, get_referral_url
from tg_bot.db_api.crud.users import select_list_users
from tg_bot.db_api.crud.chats import select_list_chats
from tg_bot.utils.functions import count_users, validate_block_bot


@dp.callback_query_handler(IsAdmin(), text="ref_urls:stats")
async def create_ml_handler(call: CallbackQuery, session: AsyncSession):
    count, ref_urls = await get_referral_urls(session)
    text = "<b>🔗 Статистика по реферальным ссылкам: </b>\n" \
           f"<b>ℹ️ Всего ссылок: </b>{count}\n\n"

    if ref_urls is not None:
        for url in ref_urls:
            text += f"❕<code>{url.name}</code> | 👤 <code>{len(url.users)}</code> | 💭 <code>{len(url.chats)}</code> | <code>/check {url.name}</code>\n"
    else:
        text += "<b>🚫 Ссылки не найдены!</b>"

    await call.message.edit_text(text, reply_markup=ref_markup)


@dp.message_handler(IsAdmin(), commands="check")
async def check_ad_handler(message: Message, session: AsyncSession):
    args = message.get_args().strip()

    if args:
        url = await get_referral_url(session, args)
        _users = await select_list_users(session, url.users)
        _chats = await select_list_chats(session, url.chats)

        counts_users = count_users(_users)
        counts_chats = count_users(_chats)
        dead_users, alive_users = await validate_block_bot(dp, url.users)

        user_url = f"https://t.me/{message.bot.config.tgbot.username}?start=ad_{args}"
        chat_url = f"https://t.me/{message.bot.config.tgbot.username}?startgroup=ad_{args}"

        await message.answer(f"<u>🔗 Статистика по реферальной ссылке {args}: </u>\n\n"
                             f"<b>👤 Всего пришло:</b> <code>{len(url.users)}</code>\n"
                             f"<b>😊 Живых:</b> <code>{len(alive_users)}</code>\n"
                             f"<b>☠️ Заблокировали:</b> <code>{len(dead_users)}</code>\n\n"
                             f"<b>➕ Прибавилось за Месяц:</b> <code>{counts_users[3]}</code>\n"
                             f"<b>➕ Прибавилось за Неделю:</b> <code>{counts_users[0]}</code>\n"
                             f"<b>➕ Прибавилось за День:</b> <code>{counts_users[1]}</code>\n"
                             f"<b>➕ Прибавилось за Час:</b> <code>{counts_users[2]}</code>\n\n"
                             f"<b>💭 Всего чатов:</b> <code>{len(url.users)}</code>\n"
                             f"<b>➕ Прибавилось за Месяц:</b> <code>{counts_chats[3]}</code>\n"
                             f"<b>➕ Прибавилось за Неделю:</b> <code>{counts_chats[0]}</code>\n"
                             f"<b>➕ Прибавилось за День:</b> <code>{counts_chats[1]}</code>\n"
                             f"<b>➕ Прибавилось за Час:</b> <code>{counts_chats[2]}</code>\n\n"
                             f"<b>🔗 Ссылки: </b>\n"
                             f"{user_url}\n"
                             f"{chat_url}"
                             )
    else:
        await message.answer("<b>🚫 Вы не ввели название реферальной ссылки!</b>")
