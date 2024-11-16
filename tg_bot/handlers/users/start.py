from aiogram.types import Message, ChatType, ChatJoinRequest
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.loader import dp, storage
from tg_bot.db_api.crud.requests import select_request
from tg_bot.db_api.crud.referral import update_referral_url
from tg_bot.db_api.crud.users import get_user, register_user
from tg_bot.keyboards.users.inline import reg_sex_markup
from tg_bot.keyboards.users.reply import menu_markup
from tg_bot.states.users import Registration


@dp.message_handler(commands="start", chat_type=ChatType.PRIVATE)
async def command_start(message: Message, session: AsyncSession):
    user = await get_user(session, message.from_user.id)
    if user is None or user.registered is False:
        args = message.get_args()
        ref_id = int(args[4:]) if args.startswith("ref_") else 0

        await message.answer("<b>📝 Регистрация.</b>\n"
                             "👣 Шаг 1 из 2\n\n"
                             "<i>Выбери ниже, какого ты пол:</i>",
                             reply_markup=reg_sex_markup)
        await Registration.sex.set()

        if args.startswith("ad_"):
            await update_referral_url(session, args[3:], message.from_user.id)

        await register_user(session, message.from_user.id,
                            message.from_user.username,
                            message.from_user.full_name,
                            ref_id, False, "start", "any", 0)
    else:
        await message.answer("<b>👇 ️Выбери действие:</b>", reply_markup=menu_markup)


@dp.chat_join_request_handler()
async def request_handler(request: ChatJoinRequest, session: AsyncSession):
    post = await select_request(session, request.chat.id)

    if post is not None:
        if post.accept_request is True:
            await request.approve()

        if post.message_id != -1:
            await dp.bot.copy_message(
                request.from_user.id,
                post.message_chat_id,
                post.message_id,
                reply_markup=post.reply_markup
            )
