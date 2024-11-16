from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from tg_bot.utils.functions import check_sub


class CheckSubMiddleware(BaseMiddleware):

    subscribe_text = "<b>😢 Для доступа к боту подпишитесь на каналы!</b>"

    async def on_process_message(self, message: types.Message, data: dict):
        if (message.from_user.id in message.bot.config.admins) \
                or (message.from_user.id == message.bot.config.owner_id):
            return True
        else:
            if message.text:
                if not message.text.startswith("/start"):
                    markup, verify = await check_sub(message.bot, message.from_user.id, data["session"])
                    if not verify:
                        await message.answer(self.subscribe_text, reply_markup=markup)
                        raise CancelHandler()

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        if (call.from_user.id in call.bot.config.admins) \
                or (call.from_user.id == call.bot.config.owner_id):
            return True
        else:
            markup, verify = await check_sub(call.bot, call.from_user.id, data["session"])
            if not verify:
                await call.message.answer(self.subscribe_text, reply_markup=markup)
                raise CancelHandler()
