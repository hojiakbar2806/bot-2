from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from tg_bot.loader import dp
from tg_bot.config import change_env
from tg_bot.states.admin import AdminsActions
from tg_bot.filters.admin_filter import IsAdmin
from tg_bot.keyboards.admin.reply import admin_markup
from tg_bot.utils.misc.set_bot_commands import set_commands
from tg_bot.keyboards.admin.inline.settings import admins_markup
from tg_bot.keyboards.admin.inline.default import cancel_markup


@dp.callback_query_handler(IsAdmin(), text="admin:admins")
async def admins_handler(call: CallbackQuery):
    text = "<u>👮‍♂️ Администраторы: </u>\n" \
           f"<code>{call.bot.config.admins}</code>"
    await call.message.edit_text(text, reply_markup=admins_markup)


@dp.callback_query_handler(IsAdmin(), text=["admin:admins:add", "admin:admins:delete"])
async def admins_actions_handler(call: CallbackQuery):
    if call.from_user.id != call.bot.config.owner_id:
        await call.answer("🚫 Вы не можете редактировать администраторов!")
    else:
        actions = {
            "admin:admins:add": [
                "<b>👮‍♂️ Введите ID Администратора для добавления: </b>",
                AdminsActions.add],
            "admin:admins:delete": [
                "<b>👮‍♂️ Введите ID Администратора для удаления: </b>",
                AdminsActions.delete]
        }

        await call.message.edit_text(actions[call.data][0],
                                     reply_markup=cancel_markup)
        await actions[call.data][1].set()


@dp.message_handler(IsAdmin(), state=AdminsActions.add)
async def admin_add_handler(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.finish()

        new_admin_id = int(message.text)

        if new_admin_id not in message.bot.config.admins:
            message.bot.config.admins += [new_admin_id, ]
            change_env("ADMINS", ", ".join([str(x) for x in message.bot.config.admins]))

            await set_commands(dp)
            await message.answer("<b>👮‍♂️ Администратор добавлен!</b>",
                                 reply_markup=admin_markup)
        else:
            await message.answer("<b>🚫 Данный ID уже есть в админ-составе!</b>",
                                 reply_markup=cancel_markup)
    else:
        await message.answer("<b>🚫 Введите ID нового администратора: </b>",
                             reply_markup=cancel_markup)


@dp.message_handler(IsAdmin(), state=AdminsActions.delete)
async def admin_delete_handler(message: Message, state: FSMContext):
    await state.finish()

    admin_id = int(message.text)

    if admin_id in message.bot.config.admins:
        message.bot.config.admins.remove(admin_id)
        change_env("ADMINS", ", ".join([str(x) for x in message.bot.config.admins]))

        await set_commands(dp)
        await message.answer("<b>👮‍♂️ Администратор удален!</b>",
                             reply_markup=admin_markup)
    else:
        await message.answer("<b>🚫 Данный ID не в админ-составе!</b>",
                             reply_markup=cancel_markup)
