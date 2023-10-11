import math
import datetime
from src.domain import task
from src.domain.fibonacci_sequence import FibonacciSequence
from src.domain.tasks_repository import TaskRepository
from src.domain.working_day_repository_collection import *
from src.domain.repository_collection import RepositoryCollection

class NotAFibonacciEstimateException(Exception):
    def __init__(self, task_id: str, *args: object) -> None:
        super().__init__(*args)
        self.task_id = task_id

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

    def lower_error(self):
        return self.expected_value - self.lower_limit

    def upper_error(self):
        return self.upper_limit - self.expected_value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ConfidenceInterval):
            return other.lower_limit == self.lower_limit and\
                other.expected_value == self.expected_value and\
                other.upper_limit == self.upper_limit
        else:
            return False

    def __str__(self) -> str:
        return self.to_string(lambda x: x)

    def to_string(self, converter) -> str:
        return f"({converter(self.lower_limit)}, {converter(self.expected_value)}, {converter(self.upper_limit)})"

class TaskReport:
    def __init__(self, sourceTask: task.Task, estimated_days: ConfidenceInterval, completion_date: ConfidenceInterval) -> None:
        self.taskId: str = sourceTask.id
        self.projectId: str = sourceTask.projectId
        self.description: str = sourceTask.description
        self.completion_date: ConfidenceInterval = completion_date
        self.estimated_days: ConfidenceInterval = estimated_days

class Report:
    def __init__(self) -> None:
        self.velocity: float = None
        self.remaining_work_days: ConfidenceInterval = None
        self.predicted_completion_dates = {} # keys: projectIds, values: completionDate: ConfidenceInterval
        self.warnings = set()
        self.task_reports = []

    def add_warnings(self, warnings):
        for w in warnings:
            self.add_warning(w)

    def add_warning(self, warning: str):
        if warning is not None:
            self.warnings.add(warning)

class ReportGenerator:
    def generate(self, repos: RepositoryCollection, startDate: datetime.date) -> Report:
        report = Report()

        task_repo = repos.task_repository

        velocity, warnings = self._calculate_recent_velocity(task_repo)
        report.add_warnings(warnings)
        report.velocity = velocity

        todo_tasks = list(filter(task.is_todo_task, task_repo.tasks.values()))

        workdays, report.task_reports, warning = self._calculate_completion_dates(todo_tasks, startDate, velocity, repos.working_days_repository_collection)
        report.add_warning(warning)
        report.remaining_work_days = workdays

        for taskReport in report.task_reports:
            # each entry might be set several times
            # the last time will set the projects completion date, because the task reports are sorted by date
            report.predicted_completion_dates[taskReport.projectId] = taskReport.completion_date

        return report

    def _calculate_recent_velocity(self, repo: TaskRepository) -> tuple[float, list]:
        tasks_for_velocity = filter(task.has_velocity, repo.tasks.values())
        sorted_tasks = sorted(tasks_for_velocity, key=lambda t: t.completedDate)
        warnings, velocity = task.calculate_velocity(sorted_tasks)

        if not velocity:
            warnings.add("No velocity could be calculated.")

        return (velocity, warnings)

    def _calculate_completion_dates(self, todoTasks: list, startDate: datetime.date, velocity: float, workingDaysRepoCollection: WorkingDayRepositoryCollection) -> tuple[float, list, str]:
        result = []

        warning = None
        workdaysSumInterval = ConfidenceInterval(0.0, 0.0, 0.0)

        for tdt in todoTasks:
            todoTask: task.Task = tdt
            
            if todoTask.estimate:
                if (not FibonacciSequence.is_in_sequence(todoTask.estimate)):
                    raise NotAFibonacciEstimateException(todoTask.id)

                estimateInterval = ConfidenceInterval(
                    FibonacciSequence.predecessor(todoTask.estimate),
                    todoTask.estimate,
                    FibonacciSequence.successor(todoTask.estimate))
                taskDurationInterval: ConfidenceInterval = estimateInterval.convert(lambda estimate: estimate / velocity)
                
                # accumulate errors according to sum-of-squares-summation
                expected_value = workdaysSumInterval.expected_value + taskDurationInterval.expected_value
                lower_limit = expected_value - math.sqrt(workdaysSumInterval.lower_error()**2 + taskDurationInterval.lower_error()**2)
                upper_limit = expected_value + math.sqrt(workdaysSumInterval.upper_error()**2 + taskDurationInterval.upper_error()**2)

                workdaysSumInterval = ConfidenceInterval(lower_limit, expected_value, upper_limit)

                # could this algorithm be optimized to use only one loop? 
                completionDateInterval = workdaysSumInterval.convert(lambda days: self._calculate_completion_date(workingDaysRepoCollection, days, startDate))

                result.append(TaskReport(todoTask, taskDurationInterval, completionDateInterval))
            else:
                warning = "Unestimated stories have been ignored."

        return (workdaysSumInterval, result, warning)

    def _calculate_completion_date(self, working_day_repo_collection: WorkingDayRepositoryCollection, remaining_days_of_work: float, start_date: datetime.date) -> datetime.date:
        if remaining_days_of_work is None:
            return None
        
        currentDate = start_date
        while remaining_days_of_work > 0:
            todays_capacity = working_day_repo_collection.get_working_day_capacity(currentDate)
            if remaining_days_of_work >= todays_capacity:
                remaining_days_of_work -= todays_capacity
                currentDate += datetime.timedelta(1)
            else:
                remaining_days_of_work = 0

        return currentDate