from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from otrs_service.configs import load_config

config = load_config('.env')

engine = create_async_engine(
    config.db.database,
    pool_size=10,
    max_overflow=20,
    pool_recycle=1800,  # Пересоздавать соединения каждые 30 минут
    pool_timeout=30,  # Ожидание свободного соединения
)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
