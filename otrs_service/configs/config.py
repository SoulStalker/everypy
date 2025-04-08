from dataclasses import dataclass
from environs import Env


@dataclass
class OtrsBaseConfig:
    database: str
    db_host: str
    db_user: str
    db_password: str


@dataclass
class KafkaConfig:
    broker: str


@dataclass
class Config:
    db: OtrsBaseConfig
    kafka: KafkaConfig


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env()

    return Config(
        db=OtrsBaseConfig(
            db_host=env('OTRS_DB_HOST'),
            database=env('OTRS_DB_URL'),
            db_user=env('OTRS_DB_USER'),
            db_password=env('OTRS_DB_PASSWORD')
        ),
        kafka=KafkaConfig(
            broker=env('KAFKA_BROKER'),
        ),
    )

