from e2_bot.domain.entities import WhatsAppContact, WhatsAppGroup, FunData

from .models import Group, Contact, Funny


def ct_model_to_dto(model: Contact) -> WhatsAppContact:
    return WhatsAppContact(
        phone_number=model.phone_number,
        first_name=model.first_name,
        last_name=model.last_name,
        email=model.email,
        telegram_id=model.telegram_id
    )


def gr_model_to_dto(model: Group) -> WhatsAppGroup:
    return WhatsAppGroup(
        group_id=model.group_id,
        group_name=model.group_name,
    )


def ct_dto_to_model(dto: WhatsAppContact) -> Contact:
    return Contact(
        phone_number=dto.phone_number,
        first_name=dto.first_name,
        last_name=dto.last_name,
        email=dto.email,
        telegram_id=dto.telegram_id,
    )


def gr_dto_to_model(dto: WhatsAppGroup) -> Group:
    return Group(
        group_id=dto.group_id,
        group_name=dto.group_name,
    )


def funny_dto_to_model(dto: FunData) -> Funny:
    return Funny(
        content_type=dto.content_type,
        file_id=dto.file_id,
        answer=dto.answer
    )


def funny_model_to_dto(model: Funny) -> FunData:
    return FunData(
        content_type=model.content_type,
        file_id=model.file_id,
        answer=model.answer
    )
