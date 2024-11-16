from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from tg_bot.db_api.crud.users import get_user


class CheckBanMiddleware(BaseMiddleware):

    banned_text = "<b>❌ Вы были заблокированы в боте!</b>"

    async def on_process_message(self, message: types.Message, data: dict):
        if (message.from_user.id not in message.bot.config.admins) \
                or (message.from_user.id != message.bot.config.owner_id):
            user = await get_user(data["session"], message.from_user.id)

            if user is not None:
                if user.ban:
                    await message.answer(self.banned_text)
                    raise CancelHandler()

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        if (call.from_user.id not in call.bot.config.admins) \
                or (call.from_user.id != call.bot.config.owner_id):
            user = await get_user(data["session"], call.from_user.id)

            if user is not None:
                if user.ban:
                    await call.message.answer(self.banned_text)
                    raise CancelHandler()
