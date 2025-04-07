from e2_bot.domain.entities.shift_message import USMessageEntity

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


# todo remove test
hia = HandleIncomingAlert()
print(hia.execute({"store_id": 40, "cashes": [1,2]}))