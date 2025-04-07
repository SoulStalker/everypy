import json

from e2_bot.domain.entities import ShopEntity
from e2_bot.domain.repositories import IShopRepository


shops_fake_db = {
    1: "Кушкина 1",
    2: "Мюллера 2",
    3: "Монтова 3",
    4: "Наполеона 4",
    5: "Слона 5",
    6: "Кота 6",
}


class JsonShops(IShopRepository):
    @staticmethod
    def get(number: int) -> ShopEntity:
        with open("shops.json", "r", encoding="utf-8") as f:
            shops = json.load(f)
            for shop in shops:
                if shop["id"] == str(number):
                    return ShopEntity(
                        number=number,
                        name=shop["address"],
                    )

