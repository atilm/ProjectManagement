from .tasks_repository import TaskRepository
from src.domain import task
from src.services.utilities import calculations

class Report:
    def __init__(self) -> None:
        self.velocity = None

class ReportGenerator:
    def generate(self, repo: TaskRepository) -> Report:
        report = Report()

        tasks_for_velocity = filter(task.has_velocity, repo.tasks.values())
        sorted_tasks = sorted(tasks_for_velocity, key=lambda t: t.completedDate)
        report.velocity = calculations.calc_average(sorted_tasks[-30:], task.calc_velocity)

        return report
