class Estimation:
    def __init__(self, min_val: float = 0.0, mode: float = 0.0, max_val: float = 0.0):
        self.min_val: float = min_val
        self.mode: float = mode
        self.max_val: float = max_val

class WorkPackage:
    def __init__(self):
        self.id: str = ""
        self.name: str = ""
        self.description: str = ""
        self.estimation: Estimation = Estimation()
        self.dependencies: list[str] = []

class Project:
    def __init__(self):
        self.name: str = ""
        self.work_packages: list[WorkPackage] = []