
class Task:
    def __init__(self, id : str, description : str) -> None:
        self.id = id
        self.description = description
        self.estimate = None
        self.createdDate = None
        self.startedDate = None
        self.completedDate = None
        self.actualWorkDays = None
        self.removedDate = None
