from aiogram.types import CallbackQuery

from tg_bot.loader import dp
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.keyboards.admin.inline.settings import botstat_markup
from tg_bot.utils.settings import change_settings, parse_settings


@dp.callback_query_handler(IsAdmin(), text="admin:botstat")
async def botstat_handler(call: CallbackQuery):
    settings = parse_settings()
    await call.message.edit_text("<u>🤖 BotStat</u>",
                                 reply_markup=botstat_markup(settings['botstat_update']))


@dp.callback_query_handler(IsAdmin(), text_startswith="botstat:auto:")
async def botstat_auto_handler(call: CallbackQuery):
    temp = True if call.data[len("botstat:auto:"):] == "on" else False
    text = "*️⃣ Авто-обновление включено" if temp else "❌ Авто-обновление выключено"

    change_settings("botstat_update", temp)
    await call.message.edit_reply_markup(botstat_markup(temp))
    await call.answer(text)
