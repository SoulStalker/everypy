from e2_bot.app.data_access.shops_json_db import JsonShops
from e2_bot.domain.services import ShopService

service = ShopService(JsonShops)

print(service.get(1))