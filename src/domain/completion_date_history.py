import datetime

from src.domain.report_generator import ConfidenceInterval

class CompletionDateRecord:
    def __init__(self, date: datetime.date, completion_date_interval: ConfidenceInterval, comment: str) -> None:
        self.date: datetime.date = date
        self.completion_date_interval = completion_date_interval
        self.comment = comment

class CompletionDateHistory:
    def __init__(self, projectId: str) -> None:
        self.projectId: str = projectId
        self.records: list[CompletionDateRecord] = []
