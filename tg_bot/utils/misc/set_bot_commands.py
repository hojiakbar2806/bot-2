from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from aiogram.dispatcher import Dispatcher

from tg_bot.utils.logger import logger


async def set_user_commands(dp: Dispatcher, user_id: int, commands: list[BotCommand]):
    try:
        await dp.bot.set_my_commands(commands,
                                     scope=BotCommandScopeChat(user_id))
    except Exception:
        logger.error(f"{user_id}: Commands are not installed.")


async def set_commands(dp: Dispatcher) -> None:

    default_commands = [
        BotCommand("start", "Запустить бота"),
    ]

    admin_commands = [
        BotCommand("admin", "[Admin] ⚒ Админ-Меню"),
        BotCommand("users", "[Admin] 🫂 Пользователи"),
        BotCommand("settings", "[Admin] ⚙️ Настройки"),
        BotCommand("ad", "[Admin] 📊 Реклама"),
        BotCommand("check", "[Admin] /check [name]")
    ]

    owners_commands = [
        BotCommand("logs", "[Owner] 🗒 Логи"),
    ]

    await dp.bot.set_my_commands(default_commands, scope=BotCommandScopeDefault())
    await set_user_commands(dp, dp.bot.config.owner_id,
                            owners_commands + admin_commands + default_commands)

    for admin_id in dp.bot.config.admins:
        await set_user_commands(dp, admin_id, admin_commands + default_commands)
