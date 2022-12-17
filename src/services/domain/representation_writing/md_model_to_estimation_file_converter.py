from collections import defaultdict

from .model_to_representation_converter import *
from src.services.markdown.markdown_document_builder import *
from src.services.markdown.markdown_document import *
from src.services.domain import markdown_configuration
from src.domain.repository_collection import RepositoryCollection

class ModelToMarkdownEstimationDocumentConverter(IModelToRepresentationConverter):
    def convert(self, repos : RepositoryCollection) -> MarkdownDocument:
        builder = MarkdownDocumentBuilder()\
            .withSection("Estimation", 0)

        tasksGroupedByEstimate = self._group_by_estimate((repos.task_repository.tasks.values()))
        keyGenerator = lambda f: -1 if f is None else f
        sortedEstimates = sorted(list(tasksGroupedByEstimate.keys()), reverse = True, key = keyGenerator)

        for estimate in sortedEstimates:
            if estimate is None:
                builder.withSection("Unestimated", 1)
                builder.withTable(self._tasks_to_table(tasksGroupedByEstimate[estimate]))
            else:
                builder.withSection(f"{estimate:g}", 1)
                builder.withTable(self._tasks_to_table(tasksGroupedByEstimate[estimate]))

        return builder.build()

    def _tasks_to_table(self, tasks: list):
        builder = MarkdownTableBuilder()\
            .withHeader(*markdown_configuration.estimation_task_header)

        for t in tasks:
            task: Task = t
            builder.withRow(task.id, task.description)

        return builder.build()

    def _group_by_estimate(self, taskList: list) -> dict:
        groups = defaultdict(list)
        for t in taskList:
            task: Task = t
            groups[task.estimate].append(task)
        
        return groups