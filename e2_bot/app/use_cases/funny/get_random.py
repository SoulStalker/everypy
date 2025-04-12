from loguru import logger


class GetRandomFunnyUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, answer: str, content_type: str = None):
        logger.debug(answer, content_type)
        return self.repository.get_random(answer, content_type)
