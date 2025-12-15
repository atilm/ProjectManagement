from projman.src.domain.repository_collection import RepositoryCollection
from projman.src.domain.working_day_repository_collection import WorkingDayRepositoryCollection
import datetime
from projman.src.domain import task

def calculate_recent_velocity(repos: RepositoryCollection) -> tuple[float, list]:
    tasksRepo = repos.task_repository
    completedTasks = filter(task.is_completed_task, tasksRepo.tasks.values())
    warnings, velocity = task.calculate_velocity(completedTasks, repos)

    if not velocity:
        warnings.add("No velocity could be calculated.")

    return (velocity, warnings)

def calculate_completion_date(working_day_repo_collection: WorkingDayRepositoryCollection, remaining_days_of_work: float, start_date: datetime.date) -> datetime.date:
    if remaining_days_of_work is None:
        return None
    
    currentDate = start_date
    while remaining_days_of_work > 0:
        todays_capacity = working_day_repo_collection.get_working_day_capacity(currentDate)
        if remaining_days_of_work >= todays_capacity:
            remaining_days_of_work -= todays_capacity
            currentDate += datetime.timedelta(1)
        else:
            remaining_days_of_work = 0

    return currentDate