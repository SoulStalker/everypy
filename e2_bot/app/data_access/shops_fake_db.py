from e2_bot.domain.entities import Shop
from e2_bot.domain.repositories import IShopRepository


shops_fake_db = {
    1: "Кушкина 1",
    2: "Мюллера 2",
    3: "Монтова 3",
    4: "Наполеона 4",
    5: "Слона 5",
    6: "Кота 6",
}


class ShopsFakeDB(IShopRepository):
    @staticmethod
    def get(number: int) -> Shop:
        return Shop(
            number=number,
            name=shops_fake_db.get(number),
        )
