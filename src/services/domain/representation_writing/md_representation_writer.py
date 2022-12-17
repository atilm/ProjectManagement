from .representation_writer import IRepresentationWriter
from .model_to_representation_converter import IModelToRepresentationConverter
from src.domain.repository_collection import RepositoryCollection
from src.services.markdown.markdown_writer import MarkdownWriter

class MarkdownRepresentationWriter(IRepresentationWriter):
    def __init__(self, converter: IModelToRepresentationConverter) -> None:
        super().__init__()
        self.converter = converter

    def write(self, repos: RepositoryCollection) -> str:
        document = self.converter.convert(repos)
        writer = MarkdownWriter()
        return writer.write(document)
