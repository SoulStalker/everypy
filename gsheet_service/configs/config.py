from dataclasses import dataclass

from environs import Env


@dataclass
class KafkaConfig:
    broker: str


@dataclass
class GSConfig:
    credentials: str
    sheet_name: str
    list_name: str


@dataclass
class Config:
    kafka: KafkaConfig
    gsheet: GSConfig


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env()

    return Config(
        kafka=KafkaConfig(
            broker=env('KAFKA_BROKER'),
        ),
        gsheet=GSConfig(
            credentials=env('CREDENTIALS_FILE'),
            sheet_name=env('SHEET_NAME'),
            list_name=env('LIST_NAME'),
        )
    )
