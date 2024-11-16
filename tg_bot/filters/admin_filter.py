from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tg_bot.utils.logger import logger


class IsAdmin(BoundFilter):
    async def check(self, obj: types.Message | types.CallbackQuery):
        logger.info(f"admin: {obj.from_user.id} -> {obj.as_json()}")

        return (obj.from_user.id in obj.bot.config.admins) \
            or (obj.from_user.id == obj.bot.config.owner_id)


class IsOwner(BoundFilter):
    async def check(self, obj: types.Message | types.CallbackQuery):
        return obj.from_user.id == obj.bot.config.owner_id
