from e2_bot.domain.repositories import IUnclosedMessageRepository


class CSIMessagesRepository(IUnclosedMessageRepository):
    pass

    # @staticmethod
    # def get_formated_message(msg: UnclosedShiftMessageEntity, shop: Shop) -> str:
    #     cashes = ",".join(map(str, msg.cashes))
    #     if len(msg.cashes) == 1:
    #         formatted_msg = f"Магазин номер {msg.shop_number},\nне закрыта смена на кассе {cashes}"
    #     else:
    #         formatted_msg = f"Магазин номер {msg.shop_number},\nне закрыта смена на кассах {cashes}"
    #     return formatted_msg