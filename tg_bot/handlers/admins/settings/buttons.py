from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from tg_bot.loader import dp
from tg_bot.states.admin import ButtonsURL
from tg_bot.utils.texts import get_buttons_info
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.utils.settings import change_settings
from tg_bot.keyboards.admin.inline.settings import buttons_markup
from tg_bot.keyboards.admin.inline.default import cancel_markup


@dp.callback_query_handler(IsAdmin(), text="admin:buttons")
async def admins_handler(call: CallbackQuery):
    text, buy_status, hide_status = await get_buttons_info()
    await call.message.edit_text(text, reply_markup=buttons_markup(buy_status, hide_status),
                                 disable_web_page_preview=True)


@dp.callback_query_handler(IsAdmin(), text_startswith="admin:button_hide:")
async def admin_button_hide_handler(call: CallbackQuery):
    temp = True if call.data[len("admin:button_hide:"):] == "on" else False
    text = "*️⃣ Кнопка Скрыть включена" if temp else "❌ Кнопка Скрыть выключена"

    settings = change_settings("buttons", temp, "hide")

    await call.message.edit_reply_markup(reply_markup=buttons_markup(settings['buttons']['buy']['active'],
                                                                     settings['buttons']['hide']))
    await call.answer(text)


@dp.callback_query_handler(IsAdmin(), text_startswith="admin:button_buy:")
async def admin_button_hide_handler(call: CallbackQuery):
    temp = True if call.data[len("admin:button_buy:"):] == "on" else False
    text = "*️⃣ Кнопка Купить включена" if temp else "❌ Кнопка Купить выключена"

    settings = change_settings("buttons", temp, "buy", "active")

    await call.message.edit_reply_markup(reply_markup=buttons_markup(settings['buttons']['buy']['active'],
                                                                     settings['buttons']['hide']))
    await call.answer(text)


@dp.callback_query_handler(IsAdmin(), text="admin:button_url:change")
async def admin_button_hide_handler(call: CallbackQuery):
    await call.message.edit_text("<b>🔗 Введите новую ссылку: </b>", reply_markup=cancel_markup)
    await ButtonsURL.new_url.set()


@dp.message_handler(IsAdmin(), state=ButtonsURL.new_url)
async def new_url_handler(message: Message, state: FSMContext):
    await state.finish()

    settings = change_settings("buttons", str(message.text), "buy", "url")

    await message.answer("<b>🔗 Новая ссылка поставлена!</b>",
                         reply_markup=buttons_markup(settings['buttons']['buy']['active'],
                                                     settings['buttons']['hide']))
