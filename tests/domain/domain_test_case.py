import unittest
import datetime
from src.domain.tasks_repository import *
from src.domain.report_generator import *
from tests.domain.domain_utilities.id_generator import IdGenerator
from src.domain.working_day_repository import WorkingDayRepository

class DomainTestCase(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self._id_generator = IdGenerator()

    def given_an_empty_repository(self) -> TaskRepository:
        return TaskRepository()

    def given_a_repository_with_tasks(self, taskList : list) -> TaskRepository:
        repo = TaskRepository()
        for t in taskList:
            repo.add(t)
        return repo

    def completed_task(self, completedDate: datetime.date, estimate: float, actualWorkDays: float) -> Task:
        task = Task(self._id_generator.next(), "")
        task.estimate = estimate
        task.actualWorkDays = actualWorkDays
        task.completedDate = completedDate
        task.startedDate = completedDate - datetime.timedelta(actualWorkDays) if actualWorkDays is not None else completedDate
        task.createdDate = task.startedDate
        return task

    def todo_task(self, estimate: float) -> Task:
        task = Task(self._id_generator.next(), "")
        task.estimate = estimate
        task.createdDate = datetime.date(2000, 1, 1)
        return task

    def when_the_user_retrieves_a_task_id(self, taskId : str, repo : TaskRepository) -> Task:
        return repo.get(taskId)

    def when_a_task_is_added(self, task : Task, repo : TaskRepository) -> Task:
        repo.add(task)

    def when_a_report_is_generated(self, task_repo: TaskRepository, startDate = datetime.date(2022, 1, 1), workdays_repo = WorkingDayRepository()) -> Report:
        generator = ReportGenerator()
        repos = RepositoryCollection(task_repo, workdays_repo)
        return generator.generate(repos, startDate)

    def then_report_generation_raises(self, repo: TaskRepository) -> Exception:
        try:
            self.when_a_report_is_generated(repo)
            self.fail("Expected an exception")
        except Exception as e:
            return e

    def then_the_repo_returns_the_task(self, taskId : str, repo : TaskRepository) -> None:
        task = repo.get(taskId)
        self.assertEqual(task.id, taskId)

    def then_the_repo_contains_estimated_task(self, taskId : str, estimate : int, repo : TaskRepository) -> None:
        task = repo.get(taskId)
        self.assertEqual(task.estimate, estimate)