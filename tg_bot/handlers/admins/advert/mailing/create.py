from aiogram.types import Message, CallbackQuery, ContentType
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.dispatcher import FSMContext
from datetime import datetime

from tg_bot.loader import dp, scheduler, storage
from tg_bot.states.admin import CreateMailing
from tg_bot.utils.mailing import mailing_users, mailing_chats
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.keyboards.admin.inline.default import cancel_markup, choose_markup
from tg_bot.db_api.crud.mailings import delete_mailing, add_mailing
from tg_bot.keyboards.admin.inline.mailing import delete_mail_markup, pin_markup


@dp.callback_query_handler(IsAdmin(), text="admin:ml:create")
async def start_mailing_create_handler(call: CallbackQuery):
    await call.message.edit_text("<b>📧 Выберите получателей: </b>",
                                 reply_markup=choose_markup)


@dp.callback_query_handler(IsAdmin(), text_startswith="mailing_choose:")
async def start_mailing_create_handler(call: CallbackQuery):
    recipients = call.data[len("mailing_choose:"):]
    await call.message.edit_text("<b>📧 Перешлите пост: </b>", reply_markup=cancel_markup)
    await CreateMailing.post.set()
    await FSMContext(storage, call.message.chat.id, call.from_user.id)\
        .update_data(recipients=recipients)


@dp.message_handler(IsAdmin(), state=CreateMailing.post, content_types=ContentType.ANY)
async def set_mailing_post_handler(message: Message, state: FSMContext):
    datetime_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    await state.update_data(message_id=message.message_id, message_chat_id=message.chat.id,
                            reply_markup=message.reply_markup.as_json() if message.reply_markup is not None else None)
    await message.answer("<b>📧 Пост выбран!</b>\n"
                         "📅 Выберите дату рассылки: \n"
                         f"🪧 <i>Пример: </i><code>{datetime_str}</code>",
                         reply_markup=cancel_markup)
    await CreateMailing.date.set()


@dp.message_handler(IsAdmin(), state=CreateMailing.date)
async def set_datetime_mailing_handler(message: Message, state: FSMContext):
    try:
        mailing_date = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
    except:
        return await message.answer("<b>❌ Вы ввели неправильную дату!</b>")

    now = datetime.now()
    if now > mailing_date:
        await message.answer("<b>❌ Вы не можете отправить рассылку раньше текущей даты!</b>")
    else:
        await state.update_data(mailing_date=mailing_date.strftime("%d.%m.%Y %H:%M:%S"))
        await message.answer("<b>📌 Закреплять сообщение рассылки у пользователей?</b>",
                             reply_markup=pin_markup)
        await CreateMailing.pin.set()


@dp.callback_query_handler(IsAdmin(), text_startswith="mailing:pin:", state=CreateMailing.pin)
async def pin_and_create_mailing_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    pin = True if call.data[len("mailing:pin:"):] == "on" else False
    data = await state.get_data()
    message = {
        "chat": {"id": data["message_chat_id"]},
        "message_id": data["message_id"],
        "reply_markup": data["reply_markup"]
    }

    await state.finish()

    run_date = datetime.strptime(data["mailing_date"], "%d.%m.%Y %H:%M:%S")

    func = mailing_users if data["recipients"] == "users" else mailing_chats
    job = scheduler.add_job(func, "date",  run_date=run_date, args=[message, pin])

    await add_mailing(session, job.id, data["message_id"], data["message_chat_id"], data["reply_markup"], run_date)
    await call.message.edit_text(f"<b>📧 Рассылка на {data['mailing_date']} была создана!</b>",
                                 reply_markup=delete_mail_markup(job.id))


@dp.callback_query_handler(IsAdmin(), text_startswith="mailing_job:delete:")
async def delete_job_handler(call: CallbackQuery, session: AsyncSession):
    job_id = call.data[len("mailing_job:delete:"):]

    try:
        scheduler.remove_job(job_id)
    except:
        pass

    await delete_mailing(session, job_id)
    await call.answer("📧 Рассылка была удалена!")
    await call.message.delete()
