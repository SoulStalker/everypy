from e2_bot.domain.services import UnclosedMessageService
from e2_bot.app.data_access.csi_messages import CSIMessagesRepository


um_service = UnclosedMessageService(CSIMessagesRepository)


