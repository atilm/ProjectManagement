from projman.src.global_settings import GlobalSettings
from projman.src.domain.report_generator import Report, TaskReport
from projman.src.domain.repository_collection import RepositoryCollection, TaskRepository
from projman.src.domain.free_range import FreeRange
from projman.src.domain import task
from projman.src.services.domain.graph_generation.graph_colors import GraphColorCycle
from projman.src.services.domain.graph_generation.xy_data import XyData
import datetime

class BurndownGraphData:
    def __init__(self) -> None:
        self.lower_confidence_band = XyData()
        self.expected_values = XyData()
        self.upper_confidence_band = XyData()
        self.free_date_ranges: FreeRange = []

    def isEmpty(self) -> bool:
        return not self.expected_values.x

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

        # filter only the most recent completed tasks
        completed_tasks = filter(task.is_completed_task, task_repo.tasks.values())
        completed_tasks = sorted(completed_tasks, key = lambda t: t.completedDate)
        completed_tasks = completed_tasks[-GlobalSettings.velocity_count:]
        remaining_effort = self._total_effort(completed_tasks, report.task_reports, task_repo)
        
        # generate graph data
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

        # filter the holidays within the plotted data point range
        if not graph_data.isEmpty():
            firstCompletionDate = graph_data.lower_confidence_band.x[0]
            lastCompletionDate = graph_data.upper_confidence_band.x[-1]

            graph_data.free_date_ranges = list(filter(
                lambda h: self._is_within_dates(h, firstCompletionDate, lastCompletionDate),
                repositories.working_days_repository_collection.get_free_ranges()))

        return graph_data

    def _is_within_dates(self, holidays: FreeRange, start_date: datetime.date, end_date: datetime.date) -> bool:
        return holidays.lastFreeDay > start_date and holidays.firstFreeDay < end_date

    def _total_effort(self, completed_tasks: list, task_reports: list, task_repo: TaskRepository) -> float:
        completed_efforts = [t.estimate for t in completed_tasks]
        todo_efforts = [self._get_estimate(task_report.taskId, task_repo) for task_report in task_reports]
        
        return sum(completed_efforts + todo_efforts, 0)

    def _get_estimate(self, task_id: str, task_repo: TaskRepository) -> float:
        return task_repo.tasks[task_id].estimate