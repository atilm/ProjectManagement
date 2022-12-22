from src.domain.report_generator import Report, TaskReport
from src.domain.repository_collection import RepositoryCollection, TaskRepository
from src.domain.working_day_repository import FreeRange
from src.domain import task
import copy

class XyData:
    def __init__(self) -> None:
        self.x = []
        self.y = []

    def append(self, x, y) -> None:
        self.x.append(x)
        self.y.append(y)

class BurndownGraphData:
    def __init__(self) -> None:
        self.lower_confidence_band = XyData()
        self.expected_values = XyData()
        self.upper_confidence_band = XyData()
        self.free_date_ranges: FreeRange = []

class BurndownGraphGenerator:
    def generate(self, report: Report, repositories: RepositoryCollection) -> BurndownGraphData:
        graph_data = BurndownGraphData()

        task_repo = repositories.task_repository

        completed_tasks = filter(task.is_completed_task, task_repo.tasks.values())
        completed_tasks = sorted(completed_tasks, key = lambda t: t.completedDate)
        remaining_effort = self._total_effort(completed_tasks, report.task_reports, task_repo)
        
        for t in completed_tasks:
            comp_task: task.Task = t
            remaining_effort -= comp_task.estimate
            graph_data.lower_confidence_band.append(comp_task.completedDate, remaining_effort)
            graph_data.expected_values.append(comp_task.completedDate, remaining_effort)
            graph_data.upper_confidence_band.append(comp_task.completedDate, remaining_effort)

        for tr in report.task_reports:
            task_report: TaskReport = tr
            remaining_effort -= self._get_estimate(task_report.taskId, task_repo)
            graph_data.lower_confidence_band.append(task_report.completion_date.lower_limit, remaining_effort)
            graph_data.expected_values.append(task_report.completion_date.expected_value, remaining_effort)
            graph_data.upper_confidence_band.append(task_report.completion_date.upper_limit, remaining_effort)

        graph_data.free_date_ranges = copy.deepcopy(repositories.working_days_repository.free_ranges)

        return graph_data

    def _total_effort(self, completed_tasks: list, task_reports: list, task_repo: TaskRepository) -> float:
        completed_efforts = [t.estimate for t in completed_tasks]
        todo_efforts = [self._get_estimate(task_report.taskId, task_repo) for task_report in task_reports]
        
        return sum(completed_efforts + todo_efforts, 0)

    def _get_estimate(self, task_id: str, task_repo: TaskRepository) -> float:
        return task_repo.tasks[task_id].estimate