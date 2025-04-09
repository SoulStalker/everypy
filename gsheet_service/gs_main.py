from loguru import logger

from app.constants.topics import KafkaTopics
from gsheet_service.service import get_data
from infrastructure.producer import send_message


def send_gs_info():
    content = get_data()
    topic = KafkaTopics.TG_BOT_MSGS.value
    payload = {"command": "EQUIPMENT", "content": content}
    logger.debug(payload)
    send_message(topic, payload)


if __name__ == "__main__":
    send_gs_info()
