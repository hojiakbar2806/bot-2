from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import CallbackQuery

from tg_bot.loader import dp
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.db_api.crud.mailings import get_mailing
from tg_bot.keyboards.admin.inline.mailing import paginate_mailing_markup, \
    mail_markup, current_mail_markup


@dp.callback_query_handler(IsAdmin(), text="admin:ml:list")
async def create_ml_handler(call: CallbackQuery, session: AsyncSession):
    await call.message.edit_text("<b>📧 Активные рассылки</b>",
                                 reply_markup=await paginate_mailing_markup(session, 0))


@dp.callback_query_handler(IsAdmin(), text_startswith="ml:pg:")
async def mailing_page_handler(call: CallbackQuery, session: AsyncSession):
    page = int(call.data[len("ml:pg:"):])
    await call.message.edit_text("<b>📧 Активные рассылки</b>",
                                 reply_markup=await paginate_mailing_markup(session, page))


@dp.callback_query_handler(IsAdmin(), text_startswith="ml:job:")
async def mailing_job_handler(call: CallbackQuery, session: AsyncSession):
    job_id = call.data[len("ml:job:"):]
    mail = await get_mailing(session, job_id)
    smile = "🚫" if mail.active is True else "✅"

    text = f"<b>{smile} Рассылка [{mail.run_date.strftime('%d.%m.%Y %H:%M:S')}]</b>\n\n" \
           f"<b>🫂 Всего: </b><code>{mail.total}</code>\n" \
           f"<b>✅ Успешно: </b><code>{mail.success}</code>\n" \
           f"<b>🚫 Не доставлено: </b><code>{mail.failed}</code>\n"

    await call.message.edit_text(text, reply_markup=await mail_markup(job_id))


@dp.callback_query_handler(IsAdmin(), text_startswith="ml:view_post:")
async def mailing_job_handler(call: CallbackQuery, session: AsyncSession):
    job_id = call.data[len("ml:view_post:"):]
    mail = await get_mailing(session, job_id)

    await dp.bot.copy_message(call.from_user.id, mail.message_chat_id,
                              mail.message_id, reply_markup=mail.markup)


@dp.callback_query_handler(IsAdmin(), text_startswith="mail:update:")
async def update_job_id_handler(call: CallbackQuery, session: AsyncSession):
    job_id = call.data[len("mail:update:"):]
    mail = await get_mailing(session, job_id)

    await call.message.edit_text(
        f"<b>📧 Рассылка на {mail.run_date.strftime('%d.%m.%Y %H:%M')} была запущена!</b>\n"
        f"<b>🫂 Всего: {mail.total}</b>\n"
        f"<b>✅ Успешно: {mail.success}</b>\n"
        f"<b>🚫 Не доставлено: {mail.failed}</b>\n",
        reply_markup=current_mail_markup(mail.job_id),
    )
