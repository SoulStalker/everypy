from e2_bot.domain.entities import WhatsAppContact


class AddContactUseCase:
    def __init__(self, repository):
        self.repository = repository

    async def execute(self, phone, first_name=None, last_name=None, email=None, telegram_id=None):
        entity = WhatsAppContact(
            phone_number=phone,
            first_name=first_name,
            last_name=last_name,
            email=email,
            telegram_id=telegram_id
        )
        wac, err = await self.repository.add(entity)
        if err:
            return err
        return wac
