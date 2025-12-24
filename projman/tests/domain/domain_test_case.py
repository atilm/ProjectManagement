import unittest
import datetime
from projman.src.domain.tasks_repository import *
from projman.src.domain.report_generator import *
from projman.tests.domain.domain_utilities.id_generator import IdGenerator
from projman.src.domain.working_day_repository_collection import *
from typing import List

class DomainTestCase(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self._id_generator = IdGenerator()

    def given_an_empty_repository(self) -> TaskRepository:
        return TaskRepository()

    def given_a_repository_with_tasks(self, taskList : List[Task]) -> TaskRepository:
        repo = TaskRepository()
        for t in taskList:
            repo.add(t)
        return repo

    def given_a_working_days_repository(self, free_weekdays: list, holidays: list, name: str = None) -> TaskRepository:
        repo = WorkingDayRepository(name) if name else WorkingDayRepository()
        repo.set_free_weekdays(*free_weekdays)
        repo.add_free_ranges(holidays)
        return repo
    
    def given_a_working_days_repository_collection(self, repositories: list[WorkingDayRepository]) -> WorkingDayRepositoryCollection:
        collection = WorkingDayRepositoryCollection()
        for repo in repositories:
            collection.add(repo)
        return collection
    
    def given_a_repository_collection(self, tasks: List[Task], working_days_repos: List[WorkingDayRepository]) -> RepositoryCollection:
        return RepositoryCollection(self.given_a_repository_with_tasks(tasks), self.given_a_working_days_repository_collection(working_days_repos))

    def completed_task(self, completedDate: datetime.date, estimate: float, actualWorkDays: float, projectId: str = "") -> Task:
        task = Task(self._id_generator.next(), "", projectId)
        task.estimate = estimate
        task.completedDate = completedDate
        task.startedDate = completedDate - datetime.timedelta(actualWorkDays - 1) if actualWorkDays is not None else completedDate
        task.createdDate = task.startedDate
        return task

    def todo_task(self, estimate: float, projectId: str = "") -> Task:
        task = Task(self._id_generator.next(), "", projectId)
        task.estimate = estimate
        task.createdDate = datetime.date(2000, 1, 1)
        return task

    def when_the_user_retrieves_a_task_id(self, taskId : str, repo : TaskRepository) -> Task:
        return repo.get(taskId)

    def when_a_task_is_added(self, task : Task, repo : TaskRepository) -> Task:
        repo.add(task)

    def when_a_report_is_generated(self, task_repo: TaskRepository, startDate = datetime.date(2022, 1, 1), *workdays_repos: WorkingDayRepository) -> Report:
        generator = ReportGenerator()
        workingDaysRepoCollection = WorkingDayRepositoryCollection()
        
        if len(workdays_repos) == 0:
            workingDaysRepoCollection.add(WorkingDayRepository())
        else:
            for repo in workdays_repos:
                workingDaysRepoCollection.add(repo)
        
        repos = RepositoryCollection(task_repo, workingDaysRepoCollection)
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
