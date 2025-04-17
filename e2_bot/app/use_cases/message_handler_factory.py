from e2_bot.app.use_cases import UCMessageHandler, WSMessageHandler, TotalMessageHandler, MessageHandler, ResultsMessageHandler
from e2_bot.domain.value_objects import UserCommand


class MessageHandlerFactory:
    handlers = {
        UserCommand.UNCLOSED.name: UCMessageHandler,
        UserCommand.TOTAL.name: TotalMessageHandler,
        UserCommand.RESULTS_BY_SHOP.name: ResultsMessageHandler,
        UserCommand.WS.name: WSMessageHandler,
    }

    @classmethod
    def get_handler(cls, message_type: str) -> MessageHandler:
        handler_class = cls.handlers.get(message_type)
        if not handler_class:
            raise ValueError(f"Unknown message type: {message_type}")
        return handler_class()
