from .model_to_representation_converter import *
from src.services.markdown.markdown_document_builder import *
from src.services.markdown.markdown_document import *

class ModelToMarkdownEstimationDocumentConverter(IModelToRepresentationConverter):
    def convert(self, repo : TaskRepository) -> MarkdownDocument:
        builder = MarkdownDocumentBuilder()\
            .withSection("Estimation", 0)

        if len(repo.tasks) != 0:
            builder.withSection("Unestimated", 1)
            builder.withTable(self._repo_to_table(repo))

        return builder.build()

    def _repo_to_table(self, repo: TaskRepository):
        builder = MarkdownTableBuilder()\
            .withHeader("Id", "Desc")

        for t in list(repo.tasks.values()):
            task: Task = t
            builder.withRow(task.id, task.description)

        return builder.build()