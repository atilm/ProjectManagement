from .model_to_representation_converter import *
from src.services.markdown.markdown_document_builder import *

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
        return self._build_table([])

    def _build_completedTable(self, repo: TaskRepository) -> MarkdownTable:
        return self._build_table([])

    def _build_removed_table(self, repo: TaskRepository) -> MarkdownTable:
        return self._build_table([])

    def _build_table(self, tasks: list) -> MarkdownTable:
        tableBuilder = MarkdownTableBuilder()\
            .withHeader("Id", "Description", "Estimate", "Started", "Completed", "Workdays", "Created", "Removed")

        for task in tasks:
            t: Task = task
            tableBuilder.withRow(t.id, t.description, t.estimate, t.startedDate, \
                t.completedDate, t.actualWorkDays, t.createdDate, t.removedDate)

        return tableBuilder.build()