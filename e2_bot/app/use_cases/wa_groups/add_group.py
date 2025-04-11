from e2_bot.domain.entities import WhatsAppGroup


class AddGroupUseCase:
    def __init__(self, repository):
        self.repository = repository

    async def execute(self, group_id, group_name):
        entity = WhatsAppGroup(
            group_id=group_id,
            group_name=group_name,
        )
        wag, err = await self.repository.add(entity)
        if err:
            return err
        return wag

