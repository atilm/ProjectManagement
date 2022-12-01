from .representation_writer import IRepresentationWriter
from .model_to_representation_converter import IModelToRepresentationConverter
from src.domain.tasks_repository import TaskRepository
from src.services.markdown.markdown_writer import MarkdownWriter

class MarkdownRepresentationWriter(IRepresentationWriter):
    def __init__(self, converter: IModelToRepresentationConverter) -> None:
        super().__init__()
        self.converter = converter

    def write(self, repo: TaskRepository) -> str:
        document = self.converter.convert(repo)
        writer = MarkdownWriter()
        return writer.write(document)
