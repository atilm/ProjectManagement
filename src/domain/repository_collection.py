from src.domain.tasks_repository import TaskRepository
from src.domain.working_day_repository_collection import *

class RepositoryCollection:
    def __init__(self, task_repository: TaskRepository, working_days_repository: WorkingDayRepositoryCollection) -> None:
        self.task_repository: TaskRepository = task_repository
        self.working_days_repository_collection: WorkingDayRepositoryCollection = working_days_repository