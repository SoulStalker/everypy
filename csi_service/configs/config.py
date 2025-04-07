from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database: str
    db_host: str
    db_user: str
    db_password: str


@dataclass
class KafkaConfig:
    broker: str


@dataclass
class Config:
    db: DatabaseConfig
    kafka: KafkaConfig


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env()

    return Config(
        db=DatabaseConfig(
            db_host=env('DB_HOST'),
            database=env('DB_URL'),
            db_user=env('DB_USER'),
            db_password=env('DB_PASSWORD')
        ),
        kafka=KafkaConfig(
            broker=env('KAFKA_BROKER'),
        ),
    )

