from projman.src.domain.repository_collection import RepositoryCollection
from .model_to_representation_converter import *
from projman.src.services.markdown.markdown_document import *
from projman.src.services.markdown.markdown_document_builder import *
from projman.src.domain.free_range import FreeRange

class CalendarFile:
    def __init__(self, filename: str, document: MarkdownDocument):
        self.filename = filename
        self.document = document

class ModelToCalendarFilesConverter:
    def convert(self, repos : RepositoryCollection) -> list[CalendarFile]:
        if not repos or not repos.working_days_repository_collection:
            return []
    
        working_days_repos = repos.working_days_repository_collection

        result = []

        for workingDaysRepo in working_days_repos.repositories:
            filename = f"{workingDaysRepo.name}.md"
            document = self._build_calendar_document(workingDaysRepo)
            calendarFile = CalendarFile(filename, document)
            result.append(calendarFile)

        return result
    
    def _build_calendar_document(self, workingDaysRepo) -> MarkdownDocument:
        documentBuilder = MarkdownDocumentBuilder()\
            .withSection(f"Calendar for {workingDaysRepo.name}", 0)\
            .withSection("Working Days", 1)\
            .withTable(self._build_working_days_table(workingDaysRepo))\
            .withSection("Holidays", 1)\
            .withTable(self._build_holidays_table(workingDaysRepo))

        return documentBuilder.build()
    
    def _build_working_days_table(self, repo) -> MarkdownTable:
        from projman.src.domain import weekdays as wd
        theWeekdays = [wd.MONDAY, wd.THURSDAY, wd.WEDNESDAY, wd.THURSDAY, wd.FRIDAY, wd.SATURDAY, wd.SUNDAY]

        markers = ["" if wd in repo.free_weekdays else "x" for wd in theWeekdays]

        return MarkdownTableBuilder()\
            .withHeader("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")\
            .withRow(*markers)\
            .build()
    
    def _build_holidays_table(self, repo: WorkingDayRepository) -> MarkdownTable:
        tableBuilder =  MarkdownTableBuilder().withHeader("Dates", "Description")

        if repo.free_ranges is None or len(repo.free_ranges) == 0:
            tableBuilder.withRow("", "")

        date_format = "%d-%m-%Y"

        for freeRange in repo.free_ranges:
            dateString = freeRange.firstFreeDay.strftime(date_format)
            if freeRange.firstFreeDay != freeRange.lastFreeDay:
                dateString += " -- " + freeRange.lastFreeDay.strftime(date_format)
            tableBuilder.withRow(dateString, freeRange.description)

        return tableBuilder.build()