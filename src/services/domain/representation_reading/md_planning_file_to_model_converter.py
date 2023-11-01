from .representation_to_model_converter import *
from src.domain.working_day_repository_collection import *
from src.domain.tasks_repository import *
from src.domain.weekdays import *
from .md_converter_exceptions import *
from src.services.markdown.markdown_document import *
from src.services.domain.task_to_string_converter import *
from src.services.utilities import string_utilities
from src.services.domain import markdown_configuration
from src.domain.repository_collection import RepositoryCollection

def parse_date_range(dateString: str, lineNumber: int) -> tuple:
    rangeMatch = GlobalSettings.date_range_regex.match(dateString)
    dateMatch = GlobalSettings.date_regex.match(dateString)

    if rangeMatch:
        firstDate = string_utilities.parse_to_date(rangeMatch.group('first'))
        lastDate = string_utilities.parse_to_date(rangeMatch.group('last'))
        return (firstDate, lastDate)
    elif dateMatch:
        d = string_utilities.parse_to_date(dateString)
        return (d, d)
    else:
        raise ValueConversionException(dateString, lineNumber)

def parse_to_free_range(tableRow: MarkdownTableRow) -> FreeRange:
        if tableRow.getColumnCount() != 2:
            raise ColumnNumberException(tableRow.lineNumber)

        dateString = tableRow.get(0).strip()
        description = tableRow.get(1).strip()
        firstDate, lastDate = parse_date_range(dateString, tableRow.lineNumber)
        return FreeRange(firstDate, lastDate, description)

class MarkdownPlanningDocumentToModelConverter(IRepresentationToModelConverter):
    def convert(self, document : MarkdownDocument) -> RepositoryCollection:
        repo = TaskRepository()
        workingDaysRepoCollection = WorkingDayRepositoryCollection()
        workingDaysRepo = WorkingDayRepository()
        hasWorkingDaysSection = False

        for item in document.getContent():
            if isinstance(item, MarkdownTable):
                if self._has_holidays_header(item):
                    hasWorkingDaysSection = True
                    free_ranges = [parse_to_free_range(r) for r in item.rows]
                    workingDaysRepo.add_free_ranges(free_ranges)
                elif self._has_working_days_header(item):
                    hasWorkingDaysSection = True
                    workingDaysRepo.set_free_weekdays(*self._to_free_days(item))
                elif self._has_tasks_header(item):
                    for row in item.rows:
                        repo.add(self._toTask(row))
                else:
                    raise HeaderFormatException(item._headerRow.lineNumber)

        if hasWorkingDaysSection:
            workingDaysRepoCollection.add(workingDaysRepo)

        return RepositoryCollection(repo, workingDaysRepoCollection)

    def _has_working_days_header(self, table: MarkdownTable):
        return self._has_header(table, markdown_configuration.planning_working_days_header)

    def _has_holidays_header(self, table: MarkdownTable):
        return self._has_header(table, markdown_configuration.planning_holidays_header)

    def _has_tasks_header(self, table: MarkdownTable):
        return self._has_header(table, markdown_configuration.planning_task_header)

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
        if row.getColumnCount() != 8:
            raise ColumnNumberException(row.lineNumber)

        try:
            return TaskToStringConverter()\
                .withId(row.get(0))\
                .withProjectId(row.get(1))\
                .withDescription(row.get(2))\
                .withEstimate(row.get(3))\
                .withStartedDate(row.get(4))\
                .withCompletedDate(row.get(5))\
                .withCreatedDate(row.get(6))\
                .withRemovedDate(row.get(7))\
                .toTask()
        except ConversionException as e:
            raise ValueConversionException(e.inputString, row.lineNumber)
