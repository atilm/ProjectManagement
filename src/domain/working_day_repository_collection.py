from .working_day_repository import WorkingDayRepository
from .free_range import FreeRange
import datetime

class WorkingDayRepositoryCollection:
    def __init__(self) -> None:
        self.repositories: list[WorkingDayRepository] = []

    def add(self, repository: WorkingDayRepository) -> None:
        self.repositories.append(repository)

    def get_working_day_capacity(self, day: datetime.date) -> float:
        """Return (N - k) / N where N is the number of workers and k the number of absent workers"""
        if len(self.repositories) == 0:
            return 0.0
        
        return sum(1 for repo in self.repositories if repo.is_working_day(day)) / len(self.repositories)
    
    def get_free_ranges(self) -> list[FreeRange]:
        return self.repositories[0].free_ranges
    