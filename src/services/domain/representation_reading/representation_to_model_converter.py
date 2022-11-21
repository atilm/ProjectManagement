from src.domain.tasks_repository import *

class IRepresentationToModelConverter:
    """This is the to convert a data source's in-memory-representation
    into the domain model"""
    def convert(source : object) -> TaskRepository:
        pass