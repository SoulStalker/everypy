from e2_bot.domain.entities.shift_message import UnclosedShiftMessageEntity

from services.unclosed_message_service import um_service
from services.shop_service import shop_service

# todo remove test
shop = shop_service.get(40)
message = UnclosedShiftMessageEntity(shop_number=40, cashes=[1, 2])
fmt_msg = um_service.get_formated_message(msg=message, shop=shop)
print(fmt_msg)