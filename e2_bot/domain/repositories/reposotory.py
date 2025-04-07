from e2_bot.domain.entities.shift_message import UnclosedShiftMessage


class IUnclosedMessageRepository:
    @staticmethod
    def format_message(msg: UnclosedShiftMessage):
        return NotImplemented
