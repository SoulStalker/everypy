class GetModelUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, pk: str):
        return self.repository.get(pk)
