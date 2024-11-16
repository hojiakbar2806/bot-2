from aiogram.types import ChatMemberUpdated
from aiogram.dispatcher.filters import BoundFilter


class IsBotAddedToGroup(BoundFilter):

    async def check(self, update: ChatMemberUpdated):
        if update.old_chat_member.user.id == update.bot.id \
                and update.new_chat_member.user.id == update.bot.id:
            if update.old_chat_member.status == "left" and update.new_chat_member.status != "left":
                return True

        return False


class IsBotKickedToGroup(BoundFilter):

    async def check(self, update: ChatMemberUpdated):
        if update.old_chat_member.user.id == update.bot.id \
                and update.new_chat_member.user.id == update.bot.id:
            if update.old_chat_member.status != "left" and update.new_chat_member.status == "left":
                return True

        return False
