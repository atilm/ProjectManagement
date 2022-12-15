from .representation_to_model_converter import *
from src.domain.working_day_repository import *
from src.domain.tasks_repository import *
from src.domain.weekdays import *
from .md_converter_exceptions import *
from src.services.markdown.markdown_document import *
from src.services.domain.task_to_string_converter import *

class MarkdownPlanningDocumentToModelConverter(IRepresentationToModelConverter):
    def convert(self, document : MarkdownDocument) -> RepositoryCollection:
        repo = TaskRepository()
        workingDaysRepo = WorkingDayRepository()

        for item in document.getContent():
            if isinstance(item, MarkdownTable):
                if self._has_holidays_header(item):
                    continue

                if self._has_working_days_header(item):
                    workingDaysRepo.set_free_weekdays(*self._to_free_days(item))
                    continue

                if not self._has_tasks_header(item):
                    raise HeaderFormatException(item._headerRow.lineNumber)

                for row in item.rows:
                    if not self._hasRequiredColumnCount(row, item):
                        raise ColumnNumberException(row.lineNumber)
                    repo.add(self._toTask(row))

        return RepositoryCollection(repo, workingDaysRepo)

    def _has_working_days_header(self, table: MarkdownTable):
        workingDaysHeaders = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        return self._has_header(table, workingDaysHeaders)

    def _has_holidays_header(self, table: MarkdownTable):
        holidaysHeaders = ["Dates", "Description"]
        return self._has_header(table, holidaysHeaders)

    def _has_tasks_header(self, table: MarkdownTable):
        expectedHeaders = ["Id", "Description", "Estimate", "Started", "Completed", "Workdays", "Created", "Removed"]
        return self._has_header(table, expectedHeaders)

    def _has_header(self, table: MarkdownTable, header: list) -> bool:
        actualHeaders = self._extract_headers(table)
        return actualHeaders == header

    def _extract_headers(self, table: MarkdownTable) -> list:
        return [table.getColumnHeader(i) for i in range(table._headerRow.getColumnCount())]

    def _hasRequiredColumnCount(self, row: MarkdownTableRow, table: MarkdownTable):
        return row.getColumnCount() == table._headerRow.getColumnCount()

    def _to_free_days(self, workingDaysTable: MarkdownTable) -> list:
        weekdays = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY]

        if workingDaysTable.getRowCount() == 0:
            raise MissingTableRowException(workingDaysTable._headerRow.lineNumber + 2)

        row: MarkdownTableRow = workingDaysTable.rows[0]

        if row.getColumnCount() != len(weekdays):
            raise ColumnNumberException(row.lineNumber)

        result = []
        for i, weekday in enumerate(weekdays):
            isWorkday = row.get(i).strip() != ""
            if not isWorkday:
                result.append(weekday)

        return result

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
