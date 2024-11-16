from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from tg_bot.utils.logger import logger


class LogMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        logger.debug(message)

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        logger.debug(call)
