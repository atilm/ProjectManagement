from src.domain.tasks_repository import *
from src.domain.working_day_repository import *
from src.domain.repository_collection import RepositoryCollection

class IModelToRepresentationConverter:
    """This is the to convert the domain model into a data source's
    in memory representation"""
    def convert(self, repos : RepositoryCollection) -> object:
        pass