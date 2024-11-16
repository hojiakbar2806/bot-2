from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.loader import dp
from tg_bot.db_api.crud.users import change_user_registered, change_user_age, change_user_sex
from tg_bot.states.users import Registration
from tg_bot.keyboards.users.reply import menu_markup


@dp.callback_query_handler(state=Registration.sex)
async def sex_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await call.message.edit_text("<b>📝 Регистрация</b>\n"
                                 "👣 Шаг 2 из 2\n\n"
                                 "<i>Напиши, cколько тебе лет? (от 10 до 99)</i>")
    await state.update_data(sex=call.data)
    await change_user_sex(session, call.from_user.id, call.data)
    await Registration.age.set()


@dp.message_handler(state=Registration.age)
async def age_handler(message: Message, state: FSMContext, session: AsyncSession):
    if message.text.isdigit() and 99 > int(message.text) > 10:

        await state.finish()

        await change_user_age(session, message.from_user.id, int(message.text))
        await change_user_registered(session, message.from_user.id, True)

        await message.answer("<b>✅ Регистрация успешно завершена</b>", reply_markup=menu_markup)
        await message.answer("<i><b>Анонимный чат бот найдет собеседника для анонимного общения по интересам и полу.</b>\n\n"
                             "Доступные команды:\n\n"
                             "👑 /prem - подробности о <b>👑 Premium статусе</b>\n"
                             "👨‍💻 /profile - посмотреть или изменить свой профиль\n"
                             "📕 /rules - правила общения в чатах\n\n"
                             "➡️ /next - следующий собеседник\n"
                             "🔎 /search - поиск собеседника\n"
                             "❌ /stop - закончить диалог\n"
                             "📲 /sharelink - отправить ссылку на ваш Telegram аккаунт\n\n"
                             "<b>Все команды всегда доступны по кнопке «Меню» в левой нижней части экрана</b>\n\n"
                             "В чатах ты можешь отправлять мне текст, ссылки, гифки, стикеры, фотографии, видео или голосовые сообщения, и я их анонимно перешлю твоему собеседнику.</i>")
    else:
        await message.answer("🚫 Введи только <b>цифры</b>: ")
