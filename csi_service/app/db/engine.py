from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from csi_service.configs import load_config

config = load_config('.env')

engine = create_async_engine(config.db.database, echo=True, future=True, poolclass=NullPool)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
