from src.domain.tasks_repository import TaskRepository

class IRepresentationWriter:
    def write(repo: TaskRepository) -> object:
        pass