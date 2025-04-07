from e2_bot.app.data_access.shops_fake_db import ShopsFakeDB
from e2_bot.domain.services import ShopService

service = ShopService(ShopsFakeDB)
