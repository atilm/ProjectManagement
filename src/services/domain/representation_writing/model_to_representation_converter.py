from src.domain.tasks_repository import *

class IModelToRepresentationConverter:
    """This is the to convert the domain model into a data source's
    in memory representation"""
    def convert(source : TaskRepository) -> object:
        pass