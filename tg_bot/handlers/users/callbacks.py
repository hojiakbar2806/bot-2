from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.loader import dp
from tg_bot.keyboards.users.inline import payment_markup, reg_sex_markup
from tg_bot.keyboards.users.reply import menu_markup
from tg_bot.states.users import ChooseSex
from tg_bot.db_api.crud.users import change_user_opposite_sex


@dp.callback_query_handler(text="hide_message", state="*")
async def hide_message_handler(call: CallbackQuery):
    await call.message.delete()


@dp.callback_query_handler(text="user:verify_required_subs", state="*")
async def verify_sub_handler(call: CallbackQuery):
    await call.message.edit_text("Меню пользователя")


@dp.callback_query_handler(text="user:back_menu", state="*")
async def verify_sub_handler(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("Меню пользователя")


@dp.callback_query_handler(text_startswith="buy_premium:")
async def buy_premium_handler(call: CallbackQuery):
    period = call.data[len("buy_premium:"):]
    await call.message.edit_text(
        "<b>Выберите платежную систему: </b>",
        reply_markup=await payment_markup(period)
    )


@dp.callback_query_handler(text="choose:opposite_sex")
async def choose_handler(call: CallbackQuery):
    await call.message.edit_text("<b>Выберите противоположный пол: </b>",
                                 reply_markup=reg_sex_markup)
    await ChooseSex.sex.set()


@dp.callback_query_handler(state=ChooseSex.sex)
async def new_sex_handler(call: CallbackQuery, session: AsyncSession,
                          state: FSMContext):
    await change_user_opposite_sex(session, call.from_user.id, call.data)
    await call.message.delete()
    await call.message.answer("<b>Вы выбрали пол собеседника</b>",
                              reply_markup=menu_markup)
    await state.finish()
