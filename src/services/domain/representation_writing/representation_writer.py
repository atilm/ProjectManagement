from src.domain.tasks_repository import TaskRepository

class IRepresentationWriter:
    def write(self, repo: TaskRepository) -> object:
        pass