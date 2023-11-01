
from src.global_settings import GlobalSettings
#from src.domain.repository_collection import RepositoryCollection
import datetime
from src.services.utilities.date_utilities import dateRange

class Task:
    def __init__(self, id: str, description: str, project_id: str) -> None:
        self.id = id
        self.projectId = project_id
        self.description = description
        self.estimate = None
        self.createdDate: datetime.date | None = None
        self.startedDate: datetime.date | None = None
        self.completedDate: datetime.date | None = None
        self.removedDate = None

class VelocityCalculationException(Exception):
    def __init__(self, task_id: str, *args: object) -> None:
        super().__init__(*args)
        self.task_id = task_id

def calculate_velocity(tasks: list[Task], repos) -> tuple[set,float]:
    """Calculate velocity from given list of tasks.
    Only take into account the globally specified number of tasks."""
    tasks_with_velocity = []
    warnings = set()

    for task in tasks:
        if has_velocity(task):
            tasks_with_velocity.append(task)
        else:
            warnings.add(GlobalSettings.no_velocity_ignored_warning.format(task.id))

    if len(tasks_with_velocity) == 0:
        return (warnings, None)

    sorted_tasks_with_velocity = sorted(tasks_with_velocity, key=lambda t: t.completedDate)


    recent_tasks: list[Task] = sorted_tasks_with_velocity[-GlobalSettings.velocity_count:]
    start_date = recent_tasks[0].startedDate
    end_date = recent_tasks[-1].completedDate

    summed_capacity = capacity_in_date_range(start_date, end_date, repos.working_days_repository_collection)

    summedEstimates = sum(t.estimate for t in recent_tasks)
    
    meanVelocity = summedEstimates / summed_capacity if summed_capacity > 0 else None

    return (warnings, meanVelocity)

def capacity_in_date_range(start_date: datetime.date, end_date: datetime.date, working_days):
    day_count = (end_date - start_date).days + 1
    if day_count < 1:
        raise VelocityCalculationException(-1)
    summed_capacity = 0

    for current_date in dateRange(start_date, end_date):
        summed_capacity += working_days.get_working_day_capacity(current_date)
    
    return summed_capacity

def has_velocity(task: Task) -> float:
    return task.estimate is not None and\
        task.startedDate is not None and\
        task.completedDate is not None and\
        task.removedDate is None

def is_todo_task(task: Task) -> bool:
    return task.completedDate == None and task.removedDate == None

def is_completed_task(task: Task) -> bool:
    return task.completedDate != None

def is_removed_task(task: Task) -> bool:
    return task.removedDate != None