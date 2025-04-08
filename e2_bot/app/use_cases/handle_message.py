from e2_bot.domain.entities.shift_message import USMessageEntity, TotalMessageEntity

from e2_bot.app.services.shop_service import shop_service


class HandleIncomingAlert:
    @classmethod
    def execute(cls, raw_data: dict):
        shop_id = raw_data["store_id"]
        cashes = raw_data["cashes"]
        shop = shop_service.get(shop_id)

        message = USMessageEntity(
            shop_number=shop_id,
            cashes=cashes,
        )
        return message.format(shop)


class HandleTotalAlert:
    @classmethod
    def execute(cls, raw_data: dict):
        sum_by_checks = raw_data["sum_by_checks"]
        checks_count = raw_data["checks_count"]
        state = raw_data["state"]
        message = TotalMessageEntity(
            sum_by_checks, checks_count, state
        )
        return message.format()
