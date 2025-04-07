from e2_bot.domain.entities.shift_message import UnclosedShiftMessageEntity
from e2_bot.domain.services import UnclosedMessageService
from e2_bot.app.data_access.csi_messages import CSIMessagesRepository

unclosed_message_service = UnclosedMessageService(CSIMessagesRepository)

message = UnclosedShiftMessageEntity(
    shop_number=2,
    cashes=[1]
)
print(unclosed_message_service.get_formated_message(message))

