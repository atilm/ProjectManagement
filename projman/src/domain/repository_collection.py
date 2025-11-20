from projman.src.domain.tasks_repository import TaskRepository
from projman.src.domain.working_day_repository_collection import *

class RepositoryCollection:
    def __init__(self, task_repository: TaskRepository, working_days_repository: WorkingDayRepositoryCollection) -> None:
        self.task_repository: TaskRepository = task_repository
        self.working_days_repository_collection: WorkingDayRepositoryCollection = working_days_repository

def mergeRepos(lhs: RepositoryCollection, rhs: RepositoryCollection) -> RepositoryCollection:
    merged_tasks = TaskRepository()
    merged_tasks.addRange(lhs.task_repository.tasks.values())
    merged_tasks.addRange(rhs.task_repository.tasks.values())

    merged_working_day_repos = WorkingDayRepositoryCollection()
    merged_working_day_repos.addRange(lhs.working_days_repository_collection.repositories)
    merged_working_day_repos.addRange(rhs.working_days_repository_collection.repositories)

    merged_repos = RepositoryCollection(merged_tasks, merged_working_day_repos)

    return merged_repos
