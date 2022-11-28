from .model_to_representation_converter import *
from src.services.markdown.markdown_document_builder import *
from src.services.domain.task_to_string_converter import *

class ModelToMarkdownPlanningDocumentConverter(IModelToRepresentationConverter):
    def convert(self, source : TaskRepository) -> object:
        document = MarkdownDocumentBuilder()\
            .withSection("Planning", 0)\
            .withSection("Stories To Do", 1)\
            .withTable(self._build_todo_table(source))\
            .withSection("Completed Stories", 1)\
            .withTable(self._build_completedTable(source))\
            .withSection("Removed Stories", 1)\
            .withTable(self._build_removed_table(source))\
            .build()
        
        return document

    def _build_todo_table(self, repo: TaskRepository) -> MarkdownTable:
        isTodoTask = lambda t: t.startedDate == None and t.removedDate == None
        todoTasks = filter(isTodoTask, list(repo.tasks.values()))
        return self._build_table(todoTasks)

    def _build_completedTable(self, repo: TaskRepository) -> MarkdownTable:
        return self._build_table([])

    def _build_removed_table(self, repo: TaskRepository) -> MarkdownTable:
        return self._build_table([])

    def _build_table(self, tasks: list) -> MarkdownTable:
        tableBuilder = MarkdownTableBuilder()\
            .withHeader("Id", "Description", "Estimate", "Started", "Completed", "Workdays", "Created", "Removed")

        converter = TaskToStringConverter()

        for task in tasks:
            fields = converter.toStrings(task) 
            tableBuilder.withRow(fields["id"], fields["description"], fields["estimate"], fields["startedDate"], \
                fields["completedDate"], fields["actualWorkDays"], fields["createdDate"], fields["removedDate"])

        return tableBuilder.build()