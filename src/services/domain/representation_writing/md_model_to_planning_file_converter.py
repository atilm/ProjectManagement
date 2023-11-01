from .model_to_representation_converter import *
from src.services.markdown.markdown_document_builder import *
from src.services.domain.task_to_string_converter import *
from src.domain.repository_collection import RepositoryCollection
from src.domain import task
from src.domain import weekdays
from src.services.utilities import string_utilities
from src.services.domain import markdown_configuration

class ModelToMarkdownPlanningDocumentConverter(IModelToRepresentationConverter):
    def convert(self, repos : RepositoryCollection) -> object:
        document = MarkdownDocumentBuilder()\
            .withSection("Planning", 0)\
            .withSection("Working Days", 1)\
            .withTable(self._build_working_days_table(repos.working_days_repository_collection.repositories[0]))\
            .withSection("Holidays", 1)\
            .withTable(self._build_holidays_table(repos.working_days_repository_collection.repositories[0]))\
            .withSection("Stories To Do", 1)\
            .withTable(self._build_todo_table(repos.task_repository))\
            .withSection("Completed Stories", 1)\
            .withTable(self._build_completedTable(repos.task_repository))\
            .withSection("Removed Stories", 1)\
            .withTable(self._build_removed_table(repos.task_repository))\
            .build()
        
        return document

    def _build_working_days_table(self, repo: WorkingDayRepository) -> MarkdownTable:
        theWeekdays = [weekdays.MONDAY, weekdays.TUESDAY, weekdays.WEDNESDAY,\
                       weekdays.THURSDAY, weekdays.FRIDAY, weekdays.SATURDAY, weekdays.SUNDAY]

        markers = ["" if wd in repo.free_weekdays else "x" for wd in theWeekdays]

        return MarkdownTableBuilder()\
            .withHeader(*markdown_configuration.planning_working_days_header)\
            .withRow(*markers)\
            .build()

    def _build_holidays_table(self, repo: WorkingDayRepository) -> MarkdownTable:
        tableBuilder =  MarkdownTableBuilder().withHeader(*markdown_configuration.planning_holidays_header)

        for freeRange in repo.free_ranges:
            beginStr = string_utilities.to_date_str(freeRange.firstFreeDay)
            endStr = string_utilities.to_date_str(freeRange.lastFreeDay)
            dateStr = f"{beginStr}" if beginStr == endStr else f"{beginStr} -- {endStr}"
            tableBuilder.withRow(dateStr, freeRange.description)

        return tableBuilder.build()

    def _build_todo_table(self, repo: TaskRepository) -> MarkdownTable:
        return self._build_table(repo, task.is_todo_task)

    def _build_completedTable(self, repo: TaskRepository) -> MarkdownTable:
        return self._build_table(repo, task.is_completed_task)

    def _build_removed_table(self, repo: TaskRepository) -> MarkdownTable:
        return self._build_table(repo, task.is_removed_task)

    def _build_table(self, repo: TaskRepository, filterPredicate) -> MarkdownTable:
        tasks = filter(filterPredicate, list(repo.tasks.values()))

        tableBuilder = MarkdownTableBuilder()\
            .withHeader(*markdown_configuration.planning_task_header)

        converter = TaskToStringConverter()

        for task in tasks:
            fields = converter.toStrings(task) 
            tableBuilder.withRow(fields["id"], fields["project"], fields["description"], fields["estimate"], fields["startedDate"], \
                fields["completedDate"], fields["createdDate"], fields["removedDate"])

        return tableBuilder.build()