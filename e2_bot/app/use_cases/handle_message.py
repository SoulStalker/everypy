import asyncio
from datetime import datetime

from loguru import logger

from e2_bot.app.services.shop_service import shop_service
from e2_bot.app.use_cases.msg_formatter import MessageFormatter
from e2_bot.domain.entities import WhatsAppMessageEntity
from e2_bot.domain.entities.sales import TotalMessageFormatter, ShopResuFormatter
from e2_bot.domain.entities.shifts import USMessageFormatter
from e2_bot.domain.value_objects.content_types import ContentTypes


class HandleIncomingAlert:
    @classmethod
    async def execute(cls, raw_data: dict):
        shop_id = raw_data["store_id"]
        cashes = raw_data["cashes"]
        shop = await shop_service.get(shop_id)
        USMessageFormatter().format(cashes, shop)
        return USMessageFormatter().format(cashes, shop)


class HandleTotalAlert:
    @classmethod
    def execute(cls, raw_data: dict):
        sum_by_checks = raw_data["sum_by_checks"]
        checks_count = raw_data["checks_count"]
        state = raw_data["state"]
        return TotalMessageFormatter().format(sum_by_checks, checks_count, state)


class HandlerResultsAlert:
    @classmethod
    def execute(cls, raw_data: dict):
        shop_id = raw_data["store_id"]
        results = raw_data["results"]
        if shop_id == "total_summary":
            return TotalMessageFormatter().format(
                sum_by_checks=results["sum_by_checks"],
                checks_count=results["checks_count"],
                state=results["state"],
            )
        else:
            shop = shop_service.get(shop_id)
            results = raw_data["results"]

            sum_by_checks = results["sum_by_checks"]
            checks_count = results["checks_count"]
            state = results["state"]
        return ShopResuFormatter().format(shop, sum_by_checks, checks_count, state)


class HandleWhatsAppAlert:
    @classmethod
    def execute(cls, raw_data: dict):
        message = WhatsAppMessageEntity(
            sender=raw_data.get("sender", ""),
            content=raw_data.get("content", ""),
            caption=raw_data.get("caption", ""),
            group=raw_data.get("group", ""),
            content_type=raw_data.get("content_type", ""),
            time_stamp=datetime.fromisoformat(raw_data.get("timestamp")),
        )
        fmt = MessageFormatter
        match message.content_type:
            case ContentTypes.TEXT.value:
                return "text", asyncio.run(fmt.execute(message))
            case ContentTypes.ETEXT.value:
                return "text", asyncio.run(fmt.execute(message))
            case ContentTypes.IMAGE.value:
                caption, filepath = message.save_media()
                caption = asyncio.run(fmt.execute(message))
                caption += message.caption
                return caption, filepath
            case ContentTypes.VIDEO.value:
                logger.error(ContentTypes.VIDEO.value)
                caption, filepath = message.save_media()
                caption = asyncio.run(fmt.execute(message))
                caption += message.caption
                return caption, filepath
            case ContentTypes.AUDIO.value:
                return "audio", "video"
            case _:
                return "other", "video"


class CleanSavedMedia:
    @classmethod
    def execute(cls):
        abc = WhatsAppMessageEntity(
            sender="",
            content="",
            group="",
            content_type="",
            time_stamp=datetime.now())
        abc.clean_media_path()
