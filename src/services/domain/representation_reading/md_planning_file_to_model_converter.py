from .representation_to_model_converter import *
from src.services.markdown.markdown_document import *
from datetime import date, datetime

class MarkdownPlanningDocumentToModelConverter(IRepresentationToModelConverter):
    def convert(self, document : MarkdownDocument) -> TaskRepository:
        repo = TaskRepository()
        
        for item in document.getContent():
            if isinstance(item, MarkdownTable):
                for row in item.rows:
                    repo.add(self._toTask(row))

        return repo

    def _toTask(self, row: MarkdownTableRow) -> Task:
        task = Task(row.get(0), row.get(1))
        task.estimate = float(row.get(2))
        task.startedDate = self._toDate(row.get(3))
        task.completedDate = self._toDate(row.get(4))
        task.actualWorkDays = float(row.get(5))
        task.createdDate = self._toDate(row.get(6))
        task.removedDate = None
        return task

    def _toDate(self, s: str) -> date:
        return datetime.strptime(s, r"%d-%m-%Y").date()

