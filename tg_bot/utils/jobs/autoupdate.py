from tg_bot.db_api.session import SessionLocal
from tg_bot.utils.functions import send_to_bot_safe, send_to_bot_man
from tg_bot.utils.settings import parse_settings


async def auto_update():
    settings = parse_settings()

    if settings["botstat_update"] is True:
        async with SessionLocal() as session:
            await send_to_bot_safe(session)
            await send_to_bot_man(session)
