from .model_to_representation_converter import *
from src.services.markdown.markdown_document_builder import *
from src.services.domain.task_to_string_converter import *
from src.domain import task

class ModelToMarkdownPlanningDocumentConverter(IModelToRepresentationConverter):
    def convert(self, source : TaskRepository) -> object:
        document = MarkdownDocumentBuilder()\
            .withSection("Planning", 0)\
            .withSection("Working Days", 1)\
            .withTable(self._build_working_days_table(source))\
            .withSection("Holidays", 1)\
            .withTable(self._build_holidays_table(source))\
            .withSection("Stories To Do", 1)\
            .withTable(self._build_todo_table(source))\
            .withSection("Completed Stories", 1)\
            .withTable(self._build_completedTable(source))\
            .withSection("Removed Stories", 1)\
            .withTable(self._build_removed_table(source))\
            .build()
        
        return document

    def _build_working_days_table(self, repo: TaskRepository) -> MarkdownTable:
        return MarkdownTableBuilder()\
            .withHeader("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")\
            .build()

    def _build_holidays_table(self, repo: TaskRepository) -> MarkdownTable:
        return MarkdownTableBuilder()\
            .withHeader("Dates", "Description")\
            .build()

    def _build_todo_table(self, repo: TaskRepository) -> MarkdownTable:
        return self._build_table(repo, task.is_todo_task)

    def _build_completedTable(self, repo: TaskRepository) -> MarkdownTable:
        return self._build_table(repo, task.is_completed_task)

    def _build_removed_table(self, repo: TaskRepository) -> MarkdownTable:
        return self._build_table(repo, task.is_removed_task)

    def _build_table(self, repo: TaskRepository, filterPredicate) -> MarkdownTable:
        tasks = filter(filterPredicate, list(repo.tasks.values()))

        tableBuilder = MarkdownTableBuilder()\
            .withHeader("Id", "Description", "Estimate", "Started", "Completed", "Workdays", "Created", "Removed")

        converter = TaskToStringConverter()

        for task in tasks:
            fields = converter.toStrings(task) 
            tableBuilder.withRow(fields["id"], fields["description"], fields["estimate"], fields["startedDate"], \
                fields["completedDate"], fields["actualWorkDays"], fields["createdDate"], fields["removedDate"])

        return tableBuilder.build()