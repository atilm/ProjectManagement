from src.domain.tasks_repository import TaskRepository
from src.domain.repository_collection import RepositoryCollection
from src.services.domain.graph_generation.xy_data import XyData
from src.domain.task import Task, is_completed_task, calculate_velocity, has_velocity
from src.services.domain.graph_generation.graph_colors import *
from src.global_settings import GlobalSettings

class EstimationErrorGraphData:
    def __init__(self) -> None:
        self.relative_errors = XyData()
        self.warnings = set()

class EstimationErrorGraphGenerator:
    def generate(self, task_repo: TaskRepository, repos: RepositoryCollection) -> EstimationErrorGraphData:
        completed_tasks = list(filter(is_completed_task, task_repo.tasks.values()))
        completed_tasks = sorted(completed_tasks, key=lambda t: t.completedDate)
        data = EstimationErrorGraphData()

        for i, t in enumerate(completed_tasks[1:], 1):
            task: Task = t

            if not task.actualWorkDays or not task.estimate:
                data.warnings.add(GlobalSettings.no_velocity_ignored_warning.format(task.id))
                continue

            warnings, velocity = calculate_velocity(completed_tasks[:i], repos)

            data.warnings = data.warnings.union(warnings)

            if not velocity:
                continue

            expectedWorkDays = task.estimate / velocity
            relative_error = (task.actualWorkDays - expectedWorkDays) / expectedWorkDays

            data.relative_errors.append(relative_error, task.estimate, GraphColorCycle.Red)

        return data
