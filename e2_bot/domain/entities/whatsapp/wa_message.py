import base64
import datetime
from dataclasses import dataclass
from pathlib import Path

from loguru import logger


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
        self.media_dir = Path("media")

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

    def clean_media_path(self):
        if self.media_dir.exists():
            for file in self.media_dir.iterdir():
                logger.info(file)
                file.unlink()

    def format(self):
        sender = self.sender.split("@")[0]
        time_stamp = self.time_stamp.strftime("%d.%m.%Y, %H:%M:%S")
        formatted_msg = f"Сообщение в группе {self.group}\n[{time_stamp}] {sender}: {self.content}"
        return formatted_msg
