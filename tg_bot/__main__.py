from aiogram import Dispatcher, executor

from tg_bot.loader import scheduler
from tg_bot.handlers import dp
from tg_bot.middleware import setup_middlewares
from tg_bot.utils.logger import setup_logger
from tg_bot.utils.misc.set_bot_commands import set_commands
from tg_bot.utils.jobs import auto_backup, auto_update, reset_premium_users
from tg_bot.utils.settings import parse_settings
from tg_bot.db_api.session import create_db_and_tables


async def on_startup(dp: Dispatcher):
    await create_db_and_tables()
    await set_commands(dp)
    await dp.bot.delete_webhook(drop_pending_updates=True)

    setup_middlewares(dp)

    settings = parse_settings()

    if settings["botstat_update"] is True:
        scheduler.add_job(
            auto_update, "cron", hour=0, id="autoupdate_1", replace_existing=True
        )

    if settings["backup"]["auto"]:
        scheduler.add_job(
            func=auto_backup,
            trigger="cron",
            hour=0,
            id="autobackup_1",
            replace_existing=True,
        )

    scheduler.add_job(
        func=reset_premium_users,
        trigger="cron",
        hour=0,
        id="reset_premium",
        replace_existing=True,
    )


async def on_shutdown(dp: Dispatcher):
    await dp.storage.close()


def start_bot():
    setup_logger("INFO", ["aiogram.bot.api"])

    scheduler.start()
    executor.start_polling(
        dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=False
    )
