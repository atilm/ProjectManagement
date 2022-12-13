from src.domain.tasks_repository import *
from src.domain.working_day_repository import *

class IModelToRepresentationConverter:
    """This is the to convert the domain model into a data source's
    in memory representation"""
    def convert(self, source : TaskRepository, workingDaysRepo: WorkingDayRepository) -> object:
        pass