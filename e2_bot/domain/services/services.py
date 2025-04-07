from e2_bot.domain.entities.shift_message import UnclosedShiftMessage
from e2_bot.domain.repositories.reposotory import IUnclosedMessageRepository


class UnclosedMessageService:
    def __init__(self, repository: IUnclosedMessageRepository):
        self.repository = repository

    def format_message(self, msg: UnclosedShiftMessage):
        return self.repository.format_message(msg)

