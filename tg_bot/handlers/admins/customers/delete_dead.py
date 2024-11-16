from aiogram.types import Message, CallbackQuery, ContentType
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.dispatcher import FSMContext

from tg_bot.loader import dp
from tg_bot.states.admin import DeleteDead
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.db_api.crud.users import delete_user
from tg_bot.keyboards.admin.inline.default import cancel_markup
from tg_bot.utils.functions import validate_block_bot, get_users_from_file


@dp.callback_query_handler(IsAdmin(), text="db:delete_dead")
async def delete_dead_handler(call: CallbackQuery):
    await call.message.edit_text("<b>☠️ Отправьте .txt файл с мертвыми: </b>",
                                 reply_markup=cancel_markup)
    await DeleteDead.file.set()


@dp.message_handler(IsAdmin(), state=DeleteDead.file,
                    content_types=ContentType.DOCUMENT)
async def delete_dead_handler(message: Message, state: FSMContext,
                              session: AsyncSession):
    await state.finish()

    read_message = await message.answer("<b>☠️ Файл принят</b>")
    path = "delete_dead_users.txt"
    text = "<b>☠️ Мертвые пользователи удалены!</b>\n\n" \
           "<b>🫂 Юзеров в файле: </b><code>{users_in_file}</code>\n" \
           "<b>🚫 Из них мертвых: </b><code>{users_dead}</code>\n" \
           "<b>✅ Найдено живых: </b><code>{users_alive}</code>"

    await message.document.download(destination_file=path)
    await read_message.edit_text("<b>☠️ Файл скачан, проверяю пользователей</b>")
    users = await get_users_from_file(path)
    dead_users, alive_users = await validate_block_bot(dp, users)

    await read_message.edit_text("<b>☠️ Пользователи проверены, удаляю...</b>")

    for user_id in dead_users:
        await delete_user(session, user_id)

    await read_message.edit_text(
        text.format(
            users_in_file=len(users),
            users_dead=len(dead_users),
            users_alive=len(alive_users)
        ))
