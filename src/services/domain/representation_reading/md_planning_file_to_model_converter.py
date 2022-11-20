from .representation_to_model_converter import *
from src.services.markdown.markdown_document import *
from datetime import date, datetime

class MarkdownConverterException(Exception):
    def __init__(self, lineNumber: int, *args: object) -> None:
        super().__init__(*args)
        self.lineNumber = lineNumber

class HeaderFormatException(MarkdownConverterException):
    pass

class ColumnNumberException(MarkdownConverterException):
    pass

class ValueConversionException(MarkdownConverterException):
    def __init__(self, inputString: str, lineNumber: int, *args: object) -> None:
        super().__init__(lineNumber, *args)
        self.inputString = inputString

class MarkdownPlanningDocumentToModelConverter(IRepresentationToModelConverter):
    def convert(self, document : MarkdownDocument) -> TaskRepository:
        repo = TaskRepository()
        
        for item in document.getContent():
            if isinstance(item, MarkdownTable):
                if not self._hasRequiredHeader(item):
                    raise HeaderFormatException(item._headerRow.lineNumber)

                for row in item.rows:
                    if not self._hasRequiredColumnCount(row, item):
                        raise ColumnNumberException(row.lineNumber)
                    repo.add(self._toTask(row))

        return repo

    def _hasRequiredHeader(self, table: MarkdownTable):
        expectedHeaders = ["Id", "Description", "Estimate", "Started", "Completed", "Workdays", "Created", "Removed"]
        actualHeaders = [table.getColumnHeader(i) for i in range(table._headerRow.getColumnCount())]

        return actualHeaders == expectedHeaders

    def _hasRequiredColumnCount(self, row: MarkdownTableRow, table: MarkdownTable):
        return row.getColumnCount() == table._headerRow.getColumnCount()

    def _toTask(self, row: MarkdownTableRow) -> Task:
        task = Task(row.get(0), row.get(1))
        task.estimate = self._convert(row, 2, self._toFloatOrNone)
        task.startedDate = self._convert(row, 3, self._toDateOrNone)
        task.completedDate = self._convert(row, 4, self._toDateOrNone)
        task.actualWorkDays = self._convert(row, 5, self._toFloatOrNone)
        task.createdDate = self._convert(row, 6, self._toDateOrNone)
        task.removedDate = self._convert(row, 7, self._toDateOrNone)
        return task

    def _convert(self, row: MarkdownTableRow, columnIndex: int, convert):
        s = row.get(columnIndex)
        try:
            return convert(s)
        except:
            raise ValueConversionException(s, row.lineNumber)

    def _toFloatOrNone(self, s: str) -> float:
        if s.strip() == "":
            return None

        return float(s)

    def _toDateOrNone(self, s: str) -> date:
        if s.strip() == "":
            return None

        return datetime.strptime(s, r"%d-%m-%Y").date()

