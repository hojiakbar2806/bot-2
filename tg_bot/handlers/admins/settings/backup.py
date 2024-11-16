from aiogram.types import CallbackQuery

from tg_bot.loader import dp
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.keyboards.admin.inline.settings import backup_markup
from tg_bot.utils.settings import parse_settings, change_settings


@dp.callback_query_handler(IsAdmin(), text="admin:backup")
async def botstat_handler(call: CallbackQuery):
    settings = parse_settings()
    await call.message.edit_text("<u>🗂 Бэкап</u>",
                                 reply_markup=backup_markup(settings['backup']['files'],
                                                            settings['backup']['users'],
                                                            settings['backup']['auto']))


@dp.callback_query_handler(IsAdmin(), text_startswith="backup:files:")
async def botstat_auto_handler(call: CallbackQuery):
    temp = True if call.data[len("backup:files:"):] == "on" else False
    text = "*️⃣ Авто-обновление файлов включено" if temp else "❌ Авто-обновление файлов выключено"

    settings = await change_settings("backup", temp, "files")

    await call.message.edit_reply_markup(backup_markup(settings['backup']['files'],
                                                       settings['backup']['users'],
                                                       settings['backup']['auto']))
    await call.answer(text)


@dp.callback_query_handler(IsAdmin(), text_startswith="backup:users:")
async def botstat_auto_handler(call: CallbackQuery):
    temp = True if call.data[len("backup:users:"):] == "on" else False
    text = "*️⃣ Авто-обновление пользователей включено" if temp else "❌ Авто-обновление пользователей выключено"

    settings = await change_settings("backup", temp, "users")

    await call.message.edit_reply_markup(backup_markup(settings['backup']['files'],
                                                       settings['backup']['users'],
                                                       settings['backup']['auto']))
    await call.answer(text)


@dp.callback_query_handler(IsAdmin(), text_startswith="backup:auto:")
async def botstat_auto_handler(call: CallbackQuery):
    temp = True if call.data[len("backup:auto:"):] == "on" else False
    text = "*️⃣ Авто-обновление включено" if temp else "❌ Авто-обновление выключено"

    settings = await change_settings("backup", temp, "auto")

    await call.message.edit_reply_markup(backup_markup(settings['backup']['files'],
                                                       settings['backup']['users'],
                                                       settings['backup']['auto']))
    await call.answer(text)
