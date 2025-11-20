from projman.src.domain.tasks_repository import *
from projman.src.domain.working_day_repository import *

class IModelToRepresentationConverter:
    """This is the to convert the domain model into a data source's
    in memory representation. E.g. RepositoryCollection to markdown document"""
    def convert(self, domain_model : object) -> object:
        pass