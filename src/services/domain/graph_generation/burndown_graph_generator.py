from src.domain.report_generator import Report, TaskReport
from src.domain.repository_collection import RepositoryCollection, TaskRepository
from src.domain.working_day_repository import FreeRange
from src.domain import task
from src.services.domain.graph_generation.graph_colors import GraphColorCycle
import copy

class XyData:
    def __init__(self) -> None:
        self.x = []
        self.y = []
        self.color = []

    def append(self, x, y, color) -> None:
        self.x.append(x)
        self.y.append(y)
        self.color.append(color)

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

        # get unique projects
        projectIds = [t.projectId for t in task_repo.tasks.values()]
        uniqueProjectIds = list(set(projectIds))
        projectIndices = {}
        for index, project in enumerate(uniqueProjectIds):
            projectIndices[project] = index

        completed_tasks = filter(task.is_completed_task, task_repo.tasks.values())
        completed_tasks = sorted(completed_tasks, key = lambda t: t.completedDate)
        remaining_effort = self._total_effort(completed_tasks, report.task_reports, task_repo)
        
        for t in completed_tasks:
            comp_task: task.Task = t
            remaining_effort -= comp_task.estimate
            graph_data.lower_confidence_band.append(comp_task.completedDate, remaining_effort, GraphColorCycle.Gray)
            graph_data.expected_values.append(comp_task.completedDate, remaining_effort, GraphColorCycle.get(projectIndices[comp_task.projectId]))
            graph_data.upper_confidence_band.append(comp_task.completedDate, remaining_effort, GraphColorCycle.Gray)

        for tr in report.task_reports:
            task_report: TaskReport = tr
            remaining_effort -= self._get_estimate(task_report.taskId, task_repo)
            graph_data.lower_confidence_band.append(task_report.completion_date.lower_limit, remaining_effort, GraphColorCycle.Gray)
            graph_data.expected_values.append(task_report.completion_date.expected_value, remaining_effort, GraphColorCycle.get(projectIndices[task_report.projectId]))
            graph_data.upper_confidence_band.append(task_report.completion_date.upper_limit, remaining_effort, GraphColorCycle.Gray)

        graph_data.free_date_ranges = copy.deepcopy(repositories.working_days_repository.free_ranges)

        return graph_data

    def _total_effort(self, completed_tasks: list, task_reports: list, task_repo: TaskRepository) -> float:
        completed_efforts = [t.estimate for t in completed_tasks]
        todo_efforts = [self._get_estimate(task_report.taskId, task_repo) for task_report in task_reports]
        
        return sum(completed_efforts + todo_efforts, 0)

    def _get_estimate(self, task_id: str, task_repo: TaskRepository) -> float:
        return task_repo.tasks[task_id].estimate