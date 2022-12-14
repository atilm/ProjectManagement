from src.domain.tasks_repository import TaskRepository
from src.domain.working_day_repository import WorkingDayRepository

class RepositoryCollection:
    def __init__(self, task_repository: TaskRepository, working_days_repository: WorkingDayRepository) -> None:
        self.task_repository = task_repository
        self.working_days_repository = working_days_repository