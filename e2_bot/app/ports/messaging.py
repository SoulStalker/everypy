from abc import ABC, abstractmethod
from typing import Protocol


class MessageSender(Protocol):
    def send(self, topic: str, message: dict) -> None:
        ...


class MessageReceiver(ABC):
    @abstractmethod
    def consume(self, handler: callable) -> None:
        ...
