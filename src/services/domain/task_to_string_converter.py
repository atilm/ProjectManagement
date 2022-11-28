
from datetime import datetime
from src.domain.task import Task

class ConversionException(Exception):
    def __init__(self, s: str, *args: object) -> None:
        super().__init__(*args)
        self.inputString = s

class TaskToStringConverter:
    def __init__(self) -> None:
        self.task = Task("", "")
        self.dateFormat = r"%d-%m-%Y"

    def withId(self, id: str):
        self.task.id = id
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

    def withActualWorkDays(self, days: str):
        self.task.actualWorkDays = self._convert(days, self._toFloatOrNone)
        return self

    def withRemovedDate(self, date: str):
        self.task.removedDate = self._convert(date, self._toDateOrNone)
        return self

    def toTask(self) -> Task:
        return self.task
    
    def toStrings(self, task: Task) -> dict:
        s = {}
        s["id"] = self._toStr(task.id, lambda s: s)
        s["description"] = self._toStr(task.description, lambda s: s)
        s["estimate"] = self._toStr(task.estimate, str)
        s["createdDate"] = self._toStr(task.createdDate, self._toDateStr)
        s["startedDate"] = self._toStr(task.startedDate, self._toDateStr)
        s["completedDate"] = self._toStr(task.completedDate, self._toDateStr)
        s["actualWorkDays"] = self._toStr(task.actualWorkDays, str)
        s["removedDate"] = self._toStr(task.removedDate, self._toDateStr)
        return s

    def _toFloatOrNone(self, s: str) -> float:
        if s.strip() == "":
            return None

        return float(s)

    def _toDateOrNone(self, s: str) -> datetime.date:
        if s.strip() == "":
            return None

        return datetime.strptime(s, self.dateFormat).date()

    def _convert(self, s: str, convert):
        try:
            return convert(s)
        except:
            raise ConversionException(s)

    def _toStr(self, obj, convert):
        if obj is None:
            return ""

        return convert(obj)

    def _toDateStr(self, date: datetime.date) -> str:
        dt = datetime.combine(date, datetime.min.time())
        return dt.strftime(self.dateFormat)