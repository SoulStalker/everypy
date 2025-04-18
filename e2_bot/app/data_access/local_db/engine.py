from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from e2_bot.configs import load_config
from .models import Base

config = load_config('.env')

engine = create_async_engine(config.db.local_db, echo=False)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
