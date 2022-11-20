from src.domain.tasks_repository import *

class IRepresentationToModelConverter:
    def convert(source : object) -> TaskRepository:
        pass