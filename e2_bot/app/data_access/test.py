from e2_bot.app.data_access.local_db.repository import WAContactRepository
from e2_bot.domain.entities import WhatsAppContact
from e2_bot.app.data_access.local_db.engine import session_maker, create_tables


async def main():
    async with session_maker() as session:
        wac = WAContactRepository(session=session)
        await create_tables()
        await wac.add(WhatsAppContact(
            ...
            # mock data
        ))


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
