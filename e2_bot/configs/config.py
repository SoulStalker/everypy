from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database: str
    local_db: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    chat_id: int
    owner_id: int


@dataclass
class KafkaConfig:
    broker: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig
    kafka: KafkaConfig


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env()

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS'))),
            chat_id=env.int('CHAT_ID'),
            owner_id=env.int('OWNER_ID'),
        ),
        db=DatabaseConfig(
            database=env('DB_URL'),
            local_db=env('LOCAL_DB'),
        ),
        kafka=KafkaConfig(
            broker=env('KAFKA_BROKER'),
        ),
    )
