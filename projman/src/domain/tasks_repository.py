from .task import Task
from typing import List

class TaskIdNotFoundException(Exception):
    pass

class TaskIdConflictException(Exception):
    def __init__(self, taskId: str, *args: object) -> None:
        super().__init__(*args)
        self.taskId = taskId

class TaskRepository:
    def __init__(self) -> None:
        self.tasks = {}

    def add(self, task : Task) -> None:
        if task.id in self.tasks:
            raise TaskIdConflictException(task.id)

        self.tasks[task.id] = task

    def addRange(self, tasks: List[Task]) -> None:
        for t in tasks:
            self.add(t)

    def get(self, taskId : str) -> Task:
        if taskId in self.tasks:
            return self.tasks[taskId]

        raise TaskIdNotFoundException

    def updateEstimate(self, task : Task) -> None:
        repoTask = self.get(task.id)
        repoTask.estimate = task.estimate

    def updateEstimates(self, taskList : list) -> None:
        for task in taskList:
            self.updateEstimate(task)