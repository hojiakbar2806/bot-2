from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.config import config
from tg_bot.utils.settings import parse_settings
from tg_bot.services.botstat.api import BotStats
from tg_bot.utils.functions import count_users

from tg_bot.db_api.crud.users import get_users, get_registered_users, \
    get_referred_users


async def get_settings_info():
    settings = parse_settings()

    backup_files = 'Включено' if settings['backup']['files'] is True else 'Отключено'
    backup_users = 'Включено' if settings['backup']['users'] is True else 'Отключено'
    backup_auto = 'Включено' if settings['backup']['auto'] is True else 'Отключено'

    text = "<u>⚙️ Настройки</u>\n\n" \
           "<b>👮‍♂️ Админ-состав:</b>\n" \
           f"\t\t\t\t\t\t<code>{config.admins}</code>\n" \
           "<b>🗂 Бэкап</b>\n" \
           f"\t\t\t\t\t\t<b>Файлов: </b><code>{backup_files}</code>\n" \
           f"\t\t\t\t\t\t<b>Юзеров: </b><code>{backup_users}</code>\n" \
           f"\t\t\t\t\t\t<b>Автоматический бэкап: </b><code>{backup_auto}</code>"

    return text


async def get_bot_info():
    text = "<i>🤖 Последняя статистика {bot_username} BotStat ({check_time}):</i>\n\n" \
           "<u>🫂 Пользователи</u>:\n" \
           "\t\t\t\t\t\t\t\tЖивы: <code>{alive_users}</code>\n" \
           "\t\t\t\t\t\t\t\tМертвы: <code>{dead_users}</code>\n" \
           "\t\t\t\t\t\t\t\tОтсутствуют: <code>{unk_users}</code>\n" \
           "\t\t\t\t\t\t\t\tПол аудитории: <code>{male} | {female}</code>\n\n" \
           "<u>💬 Чаты</u>:\n" \
           "\t\t\t\t\t\t\t\tЖивы: <code>{alive_chats}</code>\n" \
           "\t\t\t\t\t\t\t\tМертвы: <code>{dead_chats}</code>\n" \
           "\t\t\t\t\t\t\t\tПользователей в чатах: <code>{users_in_groups}</code>\n\n"

    async with BotStats(config.tgbot.token, config.bot_stat.access_token) as api:
        bot_stat = await api.get_bot_info(config.tgbot.tag)

    return text.format(
        bot_username=config.tgbot.tag,
        check_time=bot_stat.date.strftime("%d.%m.%Y %H:%M"),
        alive_users=bot_stat.users_live,
        dead_users=bot_stat.users_die,
        unk_users=bot_stat.users_empty,
        male=bot_stat.male,
        female=bot_stat.female,
        alive_chats=bot_stat.groups_live,
        dead_chats=bot_stat.groups_die,
        users_in_groups=bot_stat.users_in_groups
    )


async def get_stats_info(session: AsyncSession):
    text = "<b>⚒ Панель администратора</b>\n\n" \
           "<u>🫂 Пользователей</u>: <code>{all_users}</code>\n" \
           "\t\t\t\t\t\t➕ Прибавилось за Месяц: <code>{new_users_month}</code>\n" \
           "\t\t\t\t\t\t➕ Прибавилось за Неделю: <code>{new_users_week}</code>\n" \
           "\t\t\t\t\t\t➕ Прибавилось за День: <code>{new_users_day}</code>\n" \
           "\t\t\t\t\t\t➕ Прибавилось за Час: <code>{new_users_hour}</code>\n\n" \
           "<u>👥 Зарегистрированных пользователей</u>: <code>{all_reg_users}</code>\n" \
           "\t\t\t\t\t\t➕ Прибавилось за Месяц: <code>{reg_users_month}</code>\n" \
           "\t\t\t\t\t\t➕ Прибавилось за Неделю: <code>{reg_users_week}</code>\n" \
           "\t\t\t\t\t\t➕ Прибавилось за День: <code>{reg_users_day}</code>\n" \
           "\t\t\t\t\t\t➕ Прибавилось за Час: <code>{reg_users_hour}</code>\n\n" \
           "<u>🗣 Саморост</u>: <code>{all_ref_users}</code>\n" \
           "\t\t\t\t\t\t➕ Прибавилось за Месяц: <code>{ref_users_month}</code>\n" \
           "\t\t\t\t\t\t➕ Прибавилось за Неделю: <code>{ref_users_week}</code>\n" \
           "\t\t\t\t\t\t➕ Прибавилось за День: <code>{ref_users_day}</code>\n" \
           "\t\t\t\t\t\t➕ Прибавилось за Час: <code>{ref_users_hour}</code>\n\n"

    all_users, users = await get_users(session)
    all_reg_users, registered_users = await get_registered_users(session)
    all_ref_users, referred_users = await get_referred_users(session)

    count_new_users = count_users(users)
    count_reg_users = count_users(registered_users)
    count_ref_users = count_users(users)

    return text.format(
        all_users=all_users,
        new_users_month=count_new_users[3],
        new_users_week=count_new_users[0],
        new_users_day=count_new_users[1],
        new_users_hour=count_new_users[2],
        all_reg_users=all_reg_users,
        reg_users_month=count_reg_users[3],
        reg_users_week=count_reg_users[0],
        reg_users_day=count_reg_users[1],
        reg_users_hour=count_reg_users[2],
        all_ref_users=all_ref_users,
        ref_users_month=count_ref_users[3],
        ref_users_week=count_ref_users[0],
        ref_users_day=count_ref_users[1],
        ref_users_hour=count_ref_users[2],
    )


async def get_buttons_info():
    settings = parse_settings()

    buy_button = "Включена" if settings["buttons"]["buy"]["active"] is True else "Выключено"
    hide_button = "Включена" if settings["buttons"]["hide"] is True else "Выключено"

    text = "<b>↪️ Кнопки</b>\n" \
           f"<b>💰 Купить: </b><code>{buy_button}</code>\n" \
           f"<b>🔗 Ссылка: </b>{settings['buttons']['buy']['url']}\n" \
           f"<b>❌ Скрыть: </b><code>{hide_button}</code>"

    return text, settings['buttons']['buy']['active'], settings['buttons']['hide']


def get_service_name(service):
    services_names = {
        "qiwi_api": "Qiwi API",
        "qiwi_p2p": "Qiwi P2P",
        "lolz_pay": "Lolz",
        "crypto_pay": "CryptoBot",
        "crystal_pay": "CrystalPay",
        "freekassa": "FreeKassa"

    }
    return services_names[service]


def get_service_section(service):
    sections = {
        "qiwi_api": "QIWI_API_TOKEN",
        "qiwi_p2p": "QIWI_P2P_TOKEN",
        "crypto_pay": "CRYPTOPAY_TOKEN",
        "crystal_pay": "CRYSTALPAY_SECRET_KEY",
        "freekassa": "FK_API_KEY",
        "lolz_pay": "LOLZ_API_KEY"
    }
    return sections[service]
