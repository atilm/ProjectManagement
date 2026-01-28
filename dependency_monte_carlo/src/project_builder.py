from dependency_monte_carlo.src.project import Project, WorkPackage, Estimation

class ProjectBuilder:
    def __init__(self):
        self._project = Project()

    def set_name(self, name: str):
        self._project.name = name
        return self

    def add_work_package(self, id: str = "", name: str = "", description: str = "", estimation: Estimation = None, dependencies=None):
        wp = WorkPackage()
        wp.id = id
        wp.name = name
        wp.description = description
        wp.estimation = estimation if estimation else Estimation()
        wp.dependencies = dependencies if dependencies else []
        self._project.work_packages.append(wp)
        return self

    def build(self):
        return self._project
