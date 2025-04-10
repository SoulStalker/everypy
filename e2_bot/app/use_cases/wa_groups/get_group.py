class GetGroupUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, group_id: str):
        return self.repository.get(group_id)
