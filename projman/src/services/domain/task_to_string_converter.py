
from datetime import datetime
from projman.src.domain.task import Task
from projman.src.services.utilities import string_utilities
from projman.src.global_settings import GlobalSettings

class ConversionException(Exception):
    def __init__(self, s: str, *args: object) -> None:
        super().__init__(*args)
        self.inputString = s

class TaskToStringConverter:
    def __init__(self) -> None:
        self.task = Task("", "", "")

    def withId(self, id: str):
        self.task.id = id
        return self

    def withProjectId(self, projectId: str):
        self.task.projectId = projectId
        return self

    def withDescription(self, desc: str):
        self.task.description = desc
        return self
    
    def withEstimate(self, estimate: str):
        self.task.estimate = self._convert(estimate, self._toFloatOrNone)
        return self

    def withCreatedDate(self, date: str):
        self.task.createdDate = self._convert(date, self._toDateOrNone)
        return self

    def withStartedDate(self, date: str):
        self.task.startedDate = self._convert(date, self._toDateOrNone)
        return self

    def withCompletedDate(self, date: str):
        self.task.completedDate = self._convert(date, self._toDateOrNone)
        return self

    def withRemovedDate(self, date: str):
        self.task.removedDate = self._convert(date, self._toDateOrNone)
        return self

    def toTask(self) -> Task:
        return self.task
    
    def toStrings(self, task: Task) -> dict:
        s = {}
        s["id"] = self._toStr(task.id, lambda s: s)
        s["project"] = self._toStr(task.projectId, lambda s: s)
        s["description"] = self._toStr(task.description, lambda s: s)
        s["estimate"] = self._toStr(task.estimate, lambda f: f"{f:g}")
        s["createdDate"] = self._toStr(task.createdDate, string_utilities.to_date_str)
        s["startedDate"] = self._toStr(task.startedDate, string_utilities.to_date_str)
        s["completedDate"] = self._toStr(task.completedDate, string_utilities.to_date_str)
        s["removedDate"] = self._toStr(task.removedDate, string_utilities.to_date_str)
        return s

    def _toFloatOrNone(self, s: str) -> float:
        if s.strip() == "":
            return None

        return float(s)

    def _toDateOrNone(self, s: str) -> datetime.date:
        if s.strip() == "":
            return None

        return string_utilities.parse_to_date(s)

    def _convert(self, s: str, convert):
        try:
            return convert(s)
        except:
            raise ConversionException(s)

    def _toStr(self, obj, convert):
        if obj is None:
            return ""

        return convert(obj)