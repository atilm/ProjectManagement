from src.domain.tasks_repository import TaskRepository
from src.services.domain.graph_generation.xy_data import XyData
from src.domain.task import Task, is_completed_task, calculate_velocity, has_velocity
from src.services.utilities import calculations
from src.services.domain.graph_generation.graph_colors import *

class EstimationErrorGraphData:
    def __init__(self) -> None:
        self.relative_errors = XyData()
        self.warnings = set()

class EstimationErrorGraphGenerator:
    def generate(self, task_repo: TaskRepository) -> EstimationErrorGraphData:
        completed_tasks = list(filter(is_completed_task, task_repo.tasks.values()))
        completed_tasks = sorted(completed_tasks, key=lambda t: t.completedDate)
        data = EstimationErrorGraphData()

        for i, t in enumerate(completed_tasks[1:], 1):
            task: Task = t

            if not task.actualWorkDays or not task.estimate:
                data.warnings.add(f"Story {task.id} has no estimate or workdays and was ignored.")
                continue

            velocity = calculate_velocity(completed_tasks[:i])

            expectedWorkDays = task.estimate / velocity
            relative_error = (task.actualWorkDays - expectedWorkDays) / expectedWorkDays

            data.relative_errors.append(relative_error, task.estimate, GraphColorCycle.Red)

        return data
