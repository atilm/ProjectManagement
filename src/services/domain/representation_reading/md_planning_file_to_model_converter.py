from .representation_to_model_converter import *
from .md_converter_exceptions import *
from src.services.markdown.markdown_document import *
from src.services.domain.task_to_string_converter import *

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
        try:
            return TaskToStringConverter()\
                .withId(row.get(0))\
                .withDescription(row.get(1))\
                .withEstimate(row.get(2))\
                .withStartedDate(row.get(3))\
                .withCompletedDate(row.get(4))\
                .withActualWorkDays(row.get(5))\
                .withCreatedDate(row.get(6))\
                .withRemovedDate(row.get(7))\
                .toTask()
        except ConversionException as e:
            raise ValueConversionException(e.inputString, row.lineNumber)
