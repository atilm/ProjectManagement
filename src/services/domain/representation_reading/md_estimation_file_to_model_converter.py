from .representation_to_model_converter import *
from src.services.markdown.markdown_document import *

class MarkdownEstimationFileToModelConverter(IRepresentationToModelConverter):
    def convert(self, document: MarkdownDocument) -> TaskRepository:
        repo = TaskRepository()

        for item in document.getContent():
            if isinstance(item, MarkdownTable):
                for task in self._convert_table_to_tasks(item):
                    repo.add(task)

        return repo

    def _convert_table_to_tasks(self, table: MarkdownTable):
        for row in table.rows:
            id = row.get(0)
            description = row.get(1)
            yield Task(id, description)