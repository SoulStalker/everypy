from e2_bot.domain.entities import FunData
from e2_bot.domain.repositories import IFunDataRepository

from loguru import logger


class AddFunDataUseCase:
    def __init__(self, repository: IFunDataRepository):
        self.repository = repository

    async def execute(self, **data):
        logger.info(data)

        entity = FunData(**data)
        return await self.repository.add(entity)
