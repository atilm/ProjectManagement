from .task import Task

class TaskIdNotFoundException(Exception):
    pass

class TaskIdConflictException(Exception):
    pass

class TaskRepository:
    def __init__(self) -> None:
        self.tasks = {}

    def add(self, task : Task) -> None:
        if task.id in self.tasks:
            raise TaskIdConflictException

        self.tasks[task.id] = task

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