from e2_bot.app.use_cases import UCMessageHandler, WSMessageHandler, TotalMessageHandler, MessageHandler, ResultsMessageHandler, DefaultMessageHandler
from e2_bot.domain.value_objects import UserCommand


class MessageHandlerFactory:
    handlers = {
        UserCommand.UNCLOSED.name: UCMessageHandler,
        UserCommand.TOTAL.name: TotalMessageHandler,
        UserCommand.RESULTS_BY_SHOP.name: ResultsMessageHandler,
        UserCommand.WS.name: WSMessageHandler,
        UserCommand.OTRS_STATS.name: DefaultMessageHandler,
        UserCommand.EQUIPMENT.name: DefaultMessageHandler,
        UserCommand.OTRS_NEW_TICKET.name: DefaultMessageHandler,
    }

    @classmethod
    def get_handler(cls, message_type: str) -> MessageHandler:
        handler_class = cls.handlers.get(message_type)
        if not handler_class:
            raise ValueError(f"Unknown message type: {message_type}")
        return handler_class()
