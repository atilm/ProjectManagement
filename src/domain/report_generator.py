from .tasks_repository import TaskRepository
from src.domain import task
from src.services.utilities import calculations

class Report:
    def __init__(self) -> None:
        self.velocity = None
        self.remaining_work_days = None
        self.warnings = set()

    def add_warning(self, warning: str):
        if warning is not None:
            self.warnings.add(warning)

class ReportGenerator:
    def generate(self, repo: TaskRepository) -> Report:
        report = Report()

        velocity = self._calculate_recent_velocity(repo)

        todo_tasks = list(filter(task.is_todo_task, repo.tasks.values()))
        workdays, warning = self._calculate_workdays(todo_tasks, velocity)
        report.remaining_work_days = workdays
        report.add_warning(warning)

        report.velocity = velocity
        return report

    def _calculate_recent_velocity(self, repo: TaskRepository) -> float:
        tasks_for_velocity = filter(task.has_velocity, repo.tasks.values())
        sorted_tasks = sorted(tasks_for_velocity, key=lambda t: t.completedDate)
        return calculations.calc_average(sorted_tasks[-30:], task.calc_velocity)

    def _calculate_workdays(self, tasks: list, velocity: float) -> tuple[float, str]:
        if velocity is None:
            return (None, None)

        workdays_sum = 0
        warning = None
        for t in tasks:
            todo_task: task.Task = t
            if todo_task.estimate is not None:
                workdays_sum += todo_task.estimate / velocity
            else:
                warning = "Unestimated stories have been ignored."

        return (workdays_sum, warning)