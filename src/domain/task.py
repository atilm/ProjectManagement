
from src.services.utilities import calculations
from src.global_settings import GlobalSettings

class Task:
    def __init__(self, id: str, description: str, project_id: str) -> None:
        self.id = id
        self.projectId = project_id
        self.description = description
        self.estimate = None
        self.createdDate = None
        self.startedDate = None
        self.completedDate = None
        self.actualWorkDays = None
        self.removedDate = None

class VelocityCalculationException(Exception):
    def __init__(self, task_id: str, *args: object) -> None:
        super().__init__(*args)
        self.task_id = task_id

def calc_velocity(task: Task) -> float:
    if task.actualWorkDays <= 0:
        raise VelocityCalculationException(task.id)

    return task.estimate / task.actualWorkDays

def calculate_velocity(sorted_task_list: list) -> tuple[set,float]:
    """Calculate velocity from given list of tasks.
    Only take into account the global specified number of tasks.
    Therefore the INPUT MUST BE SORTED by completion date."""
    tasks_with_velocity = []
    warnings = set()

    for task in sorted_task_list:
        if has_velocity(task):
            tasks_with_velocity.append(task)
        else:
            warnings.add(GlobalSettings.no_velocity_ignored_warning.format(task.id))

    averageVelocity = calculations.calc_average(tasks_with_velocity[-GlobalSettings.velocity_count:], calc_velocity)

    return (warnings, averageVelocity)

def has_velocity(task: Task) -> float:
    return task.estimate is not None and\
        task.actualWorkDays is not None and\
        task.removedDate is None

def is_todo_task(task: Task) -> bool:
    return task.completedDate == None and task.removedDate == None

def is_completed_task(task: Task) -> bool:
    return task.completedDate != None

def is_removed_task(task: Task) -> bool:
    return task.removedDate != None