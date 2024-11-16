from dataclasses import dataclass
from environs import Env

env = Env()
env.read_env("./data/.env")


@dataclass
class Database:
    host: str
    port: int
    user: str
    password: str
    name: str
    db_uri: str
    apscheduler_uri: str


@dataclass
class Redis:
    host: str
    port: str
    password: str | None


@dataclass
class Bot:
    token: str
    tag: str
    username: str


@dataclass
class BotStat:
    access_token: str


@dataclass
class QiwiApiConfig:
    token: str | None
    phone: str | None
    nick: str | None


@dataclass
class QiwiP2PConfig:
    token: str | None


@dataclass
class LolzPayment:
    username: str | None
    api_key: str | None


@dataclass
class CrystalPayment:
    secret_key: str | None
    name: str | None


@dataclass
class QiwiPayment:
    qiwi_api: QiwiApiConfig | None
    qiwi_p2p: QiwiP2PConfig | None


@dataclass
class Payments:
    qiwi: QiwiPayment | None
    lolz: LolzPayment | None
    crystalpay: CrystalPayment | None


@dataclass
class Config:
    tgbot: Bot
    db: Database
    redis: Redis
    payments: Payments
    bot_stat: BotStat

    admins: list
    owner_id: int


def change_env(section: str, value: str):
    dumped_env = env.dump()
    text = ""

    with open("./data/.env", "w", encoding="utf-8") as file:
        for v in dumped_env:
            if v:
                e = dumped_env[v]

                if v == section:
                    e = value

                text += f"{v}={e}\n"

        file.write(text)


try:
    admins = list(map(int, env.str("ADMINS").split(",")))
except ValueError:
    admins = [int(x) for x in env.str("ADMINS").split(",") if x]

db_uri = f"postgresql+asyncpg://" \
         f"{env.str('DB_USER')}:{env.str('DB_PASSWORD')}@" \
         f"{env.str('DB_HOST')}:{env.int('DB_PORT')}" \
         f"/{env.str('DB_NAME')}"

apscheduler_uri = f"postgresql://" \
         f"{env.str('DB_USER')}:{env.str('DB_PASSWORD')}@" \
         f"{env.str('DB_HOST')}:{env.int('DB_PORT')}" \
         f"/{env.str('DB_NAME')}"

config = Config(
    tgbot=Bot(
        token=env.str("BOT_TOKEN"),
        tag=env.str("BOT_TAG"),
        username=env.str("BOT_TAG")[1:]
    ),
    db=Database(
        host=env.str("DB_HOST"),
        port=env.int("DB_PORT"),
        user=env.str("DB_USER"),
        password=env.str("DB_PASSWORD"),
        name=env.str("DB_NAME"),
        db_uri=db_uri,
        apscheduler_uri=apscheduler_uri
    ),
    redis=Redis(
        host=env.str("REDIS_HOST"),
        port=env.int("REDIS_PORT"),
        password=env.str("REDIS_PASSWORD")
    ),
    payments=Payments(
        qiwi=QiwiPayment(
            qiwi_api=QiwiApiConfig(
                token=env.str("QIWI_API_TOKEN"),
                phone=env.str("QIWI_API_PHONE"),
                nick=env.str("QIWI_API_NICKNAME")
            ),
            qiwi_p2p=QiwiP2PConfig(token=env.str("QIWI_P2P_TOKEN"))
        ),
        lolz=LolzPayment(
            username=env.str("LOLZ_USERNAME"),
            api_key=env.str("LOLZ_API_KEY"),
        ),
        crystalpay=CrystalPayment(
            secret_key=env.str("CRYSTALPAY_SECRET_KEY"),
            name=env.str("CRYSTALPAY_NAME")
        ),
    ),
    admins=admins,
    owner_id=env.int("OWNER_ID"),
    bot_stat=BotStat(
        access_token=env.str("BOTSTAT_TOKEN")
    )
)
