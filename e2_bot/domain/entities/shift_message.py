import base64
import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

from loguru import logger

from e2_bot.domain.entities import ShopEntity


@dataclass
class USMessageEntity:
    shop_number: int
    cashes: [int]

    def format(self, shop: ShopEntity):
        cashes = ", ".join(map(str, self.cashes))
        if shop:
            if len(self.cashes) == 0:
                formatted_msg = f"Все смены закрыты"
            elif len(self.cashes) == 1:
                formatted_msg = f"{shop.name},\nне закрыта смена на кассе {cashes}"
            else:
                formatted_msg = f"{shop.name},\nне закрыта смена на кассах {cashes}"
        else:
            formatted_msg = f"Проблема с получением адреса магазина"
        return formatted_msg


@dataclass
class TotalMessageEntity:
    sum_by_checks: float
    checks_count: int
    state: str

    def format(self):
        formatted_msg = (
            f"Суммарный отчет за {datetime.date.today()}:\n"
            f"Чеки: {self.checks_count} шт\n"
            f"Оборот: {self.sum_by_checks:.2f} руб."
        )
        if self.state != "{0}":
            return formatted_msg
        else:
            return f"{formatted_msg}\n(не во всех магазинах закрыты смены)."


@dataclass
class ShopResultEntity:
    sum_by_checks: float
    checks_count: int
    state: str

    def format(self, shop: ShopEntity):
        formatted_msg = (
            f"Суммарный отчет за {datetime.date.today()}:\n"
            f"Чеки: {self.checks_count} шт\n"
            f"Оборот: {self.sum_by_checks:.2f} руб."
        )
        if self.state != "{0}":
            return formatted_msg
        else:
            return f"{formatted_msg}\n(в магазине не все смены закрыты)."


@dataclass
class WhatsAppMessageEntity:
    def __init__(
            self,
            sender: str,
            content: str,
            group: str,
            content_type: str,
            time_stamp: datetime.datetime
    ):
        self.sender = sender
        self.content = content
        self.group = group
        self.content_type = content_type
        self.time_stamp = time_stamp
        self.media_dir = Path("media")  # Путь к папке

    def save_media(self) -> tuple[str, str | None]:
        caption = f"Сообщение в группе {self.group}\n[{self.time_stamp.strftime('%d.%m.%Y, %H:%M:%S')}] {self.sender}:"
        """Декодирует base64 и сохраняет в папку media. Возвращает путь к файлу."""
        try:
            # 1. Создаем папку, если ее нет
            self.media_dir.mkdir(exist_ok=True)
            # 2. Генерируем уникальное имя файла
            filename = (
                f"{self.time_stamp.strftime('%Y%m%d_%H%M%S')}"
                f"_{self.sender.replace(' ', '_')}.jpg"  # или другой формат
            )
            # 3. Декодируем base64
            media_bytes = base64.b64decode(self.content)
            # 4. Сохраняем файл
            filepath = self.media_dir / filename
            with open(filepath, "wb") as f:
                f.write(media_bytes)

            logger.info(f"Media saved: {filepath}")
            return caption, str(filepath)

        except (TypeError, ValueError) as e:
            logger.error(f"Base64 decode error: {str(e)}")
        except Exception as e:
            logger.error(f"Media save failed: {str(e)}", exc_info=True)
        return caption, None

    def format(self):
        sender = self.sender.split("@")[0]
        time_stamp = self.time_stamp.strftime("%d.%m.%Y, %H:%M:%S")
        # time_stamp = self.time_stamp.split("T")[0]
        formatted_msg = f"Сообщение в группе {self.group}\n[{time_stamp}] {sender}: {self.content}"
        return formatted_msg
