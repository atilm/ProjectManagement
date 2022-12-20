from src.domain import task
from src.domain.fibonacci_sequence import FibonacciSequence
from src.services.utilities import calculations
import datetime
from src.domain.tasks_repository import TaskRepository
from src.domain.working_day_repository import WorkingDayRepository
from src.domain.repository_collection import RepositoryCollection

class ConfidenceInterval:
    def __init__(self, lower_limit, expected_value, upper_limit) -> None:
        self.lower_limit = lower_limit
        self.expected_value = expected_value
        self.upper_limit = upper_limit

    def convert(self, conversion): # -> ConfidenceInterval
        return ConfidenceInterval(
            conversion(self.lower_limit),
            conversion(self.expected_value),
            conversion(self.upper_limit)
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ConfidenceInterval):
            return other.lower_limit == self.lower_limit and\
                other.expected_value == self.expected_value and\
                other.upper_limit == self.upper_limit
        else:
            return False

    def __str__(self) -> str:
        return f"({self.lower_limit}, {self.expected_value}, {self.upper_limit})"

class TaskReport:
    def __init__(self, sourceTask: task.Task, estimated_days: float, completion_date: datetime.date) -> None:
        self.taskId = sourceTask.id
        self.description = sourceTask.description
        self.completion_date = completion_date
        self.estimated_days = estimated_days

class Report:
    def __init__(self) -> None:
        self.velocity: float = None
        self.remaining_work_days: float = None
        self.predicted_completion_date: ConfidenceInterval = None
        self.warnings = set()
        self.task_reports = []

    def add_warning(self, warning: str):
        if warning is not None:
            self.warnings.add(warning)

class ReportGenerator:
    def generate(self, repos: RepositoryCollection, startDate: datetime.date) -> Report:
        report = Report()

        task_repo = repos.task_repository

        velocity, warning = self._calculate_recent_velocity(task_repo)
        report.add_warning(warning)
        report.velocity = velocity

        todo_tasks = list(filter(task.is_todo_task, task_repo.tasks.values()))

        workdays, report.task_reports, warning = self._calculate_completion_dates(todo_tasks, startDate, velocity, repos.working_days_repository)
        report.add_warning(warning)
        report.remaining_work_days = workdays
        if report.task_reports:
            report.predicted_completion_date = report.task_reports[-1].completion_date

        return report

    def _calculate_recent_velocity(self, repo: TaskRepository) -> tuple[float, str]:
        tasks_for_velocity = filter(task.has_velocity, repo.tasks.values())
        sorted_tasks = sorted(tasks_for_velocity, key=lambda t: t.completedDate)
        velocity =  calculations.calc_average(sorted_tasks[-30:], task.calc_velocity)

        warning = None if velocity else "No velocity could be calculated."

        return (velocity, warning)

    def _calculate_completion_dates(self, todoTasks: list, startDate: datetime.date, velocity: float, workingDaysRepo: WorkingDayRepository) -> tuple[float, list, str]:
        result = []

        warning = None
        workdaysSum = 0

        for tdt in todoTasks:
            todoTask: task.Task = tdt
            
            if todoTask.estimate:
                estimateInterval = ConfidenceInterval(
                    FibonacciSequence.predecessor(todoTask.estimate),
                    todoTask.estimate,
                    FibonacciSequence.successor(todoTask.estimate))
                taskDurationInterval: ConfidenceInterval = estimateInterval.convert(lambda estimate: estimate / velocity)
                workdaysSum += taskDurationInterval.expected_value
                # could this algorithm be optimized to use only one loop? 
                completion_date = self._calculate_completion_date(workingDaysRepo, workdaysSum, startDate)

                completionDateInterval = ConfidenceInterval(None, completion_date, None)
                result.append(TaskReport(todoTask, taskDurationInterval, completionDateInterval))
            else:
                warning = "Unestimated stories have been ignored."

        return (workdaysSum, result, warning)

    def _calculate_completion_date(self, working_day_repo: WorkingDayRepository, days_of_work: float, start_date: datetime.date) -> datetime.date:
        if days_of_work is None:
            return None
        
        currentDate = start_date
        while days_of_work > 0:
            if not working_day_repo.is_working_day(currentDate):
                currentDate += datetime.timedelta(1)
            else:
                if days_of_work >= 1:
                    days_of_work -= 1
                    currentDate += datetime.timedelta(1)
                else:
                    days_of_work = 0

        return currentDate