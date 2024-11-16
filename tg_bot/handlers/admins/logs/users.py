import os

from aiogram.types import Message, CallbackQuery, InputFile
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.dispatcher import FSMContext

from tg_bot.loader import dp
from tg_bot.filters.admin_filter import IsOwner
from tg_bot.utils.functions import dump_users_to_file
from tg_bot.keyboards.admin.inline.default import logs_markup
from tg_bot.utils.jobs.autobackup import backup_users, backup_files, backup_configs


@dp.message_handler(IsOwner(), commands="logs", state="*")
@dp.message_handler(IsOwner(), text="🗒 Логи", state="*")
async def command_start(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("<u>🗒 Логи</u>", reply_markup=logs_markup)


@dp.callback_query_handler(IsOwner(), text="owner:backup:users:txt")
async def backup_users_handler(call: CallbackQuery, session: AsyncSession):
    path = await dump_users_to_file(session)
    await call.message.answer_document(InputFile(path), caption="<b>🗒 Выгрузка пользователей в .txt</b>")
    os.remove(path)


@dp.callback_query_handler(IsOwner(), text="owner:backup:users:sql")
async def backup_users_handler(call: CallbackQuery):
    path = await backup_users()
    await call.message.answer_document(InputFile(path), caption="<b>🗒 Выгрузка пользователей в .sql</b>")
    os.remove(path)


@dp.callback_query_handler(IsOwner(), text="owner:backup:files")
async def backup_files_handler(call: CallbackQuery):
    path = await backup_files()
    await call.message.answer_document(InputFile(path), caption="<b>🗒 Выгрузка файлов</b>")
    os.remove(path)


@dp.callback_query_handler(IsOwner(), text="owner:backup:configs")
async def backup_files_handler(call: CallbackQuery):
    path = await backup_configs()
    await call.message.answer_document(InputFile(path), caption="<b>🗒 Выгрузка конфигов и логов</b>")
    os.remove(path)
