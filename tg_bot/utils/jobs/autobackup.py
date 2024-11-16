import os
import shutil

from sqlalchemy import text
from aiogram.types import InputFile, InputMediaDocument, MediaGroup

from tg_bot.loader import dp
from tg_bot.utils.settings import parse_settings
from tg_bot.db_api.session import SessionLocal


async def backup_files():
    shutil.make_archive("backup_files", 'zip', "./tg_bot/")
    return "./backup_files.zip"


async def backup_configs():
    shutil.make_archive("backup_data", 'zip', "./data/")
    return "./backup_data.zip"


async def backup_users():
    async with SessionLocal() as session:
        query = await session.execute(text("select * from users"))
        f = open('./backup_users.sql', 'w', encoding="utf-8")

        try:
            for row in query:
                f.write(f"insert into users values ({row});\n")
        except Exception as e:
            print('Error %s' % e)

        f.close()

    return "./backup_users.sql"


async def send_backup_files(backup_paths):
    medias = [InputMediaDocument(InputFile(path)) for path in backup_paths]
    medias[0].caption = "<b>⏳ Бэкап файлов</b>"

    try:
        await dp.bot.send_media_group(dp.bot.config.owner_id, MediaGroup(medias))
    except:
        pass


async def auto_backup():
    settings = parse_settings()
    backup_paths = []

    if settings["backup"]["files"] is True:
        files_path = await backup_files()
        backup_paths.append(files_path)

    if settings["backup"]["users"] is True:
        users_path = await backup_users()
        backup_paths.append(users_path)

    await send_backup_files(backup_paths)

    for path in backup_paths:
        os.remove(path)