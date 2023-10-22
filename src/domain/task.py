
from src.services.utilities import calculations
from src.global_settings import GlobalSettings
#from src.domain.repository_collection import RepositoryCollection
import datetime

class Task:
    def __init__(self, id: str, description: str, project_id: str) -> None:
        self.id = id
        self.projectId = project_id
        self.description = description
        self.estimate = None
        self.createdDate: datetime.date | None = None
        self.startedDate: datetime.date | None = None
        self.completedDate: datetime.date | None = None
        self.actualWorkDays = None
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
    day_count = (end_date - start_date).days + 1

    if day_count < 1:
        raise VelocityCalculationException(recent_tasks[-1].id)

    summed_capacity = 0
    working_days = repos.working_days_repository_collection

    for current_date in (start_date + datetime.timedelta(n) for n in range(day_count)):
        summed_capacity += working_days.get_working_day_capacity(current_date)

    summedEstimates = sum(t.estimate for t in recent_tasks)
    
    meanVelocity = summedEstimates / summed_capacity if summed_capacity > 0 else None

    return (warnings, meanVelocity)

def has_velocity(task: Task) -> float:
    return task.estimate is not None and\
        task.startedDate is not None and\
        task.completedDate is not None and\
        task.actualWorkDays is not None and\
        task.removedDate is None

def is_todo_task(task: Task) -> bool:
    return task.completedDate == None and task.removedDate == None

def is_completed_task(task: Task) -> bool:
    return task.completedDate != None

def is_removed_task(task: Task) -> bool:
    return task.removedDate != None