from src.domain.tasks_repository import TaskRepository

class IRepresentationReader:
    def read(source: object) -> TaskRepository:
        pass