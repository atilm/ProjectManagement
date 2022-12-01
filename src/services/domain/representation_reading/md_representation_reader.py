from .representation_to_model_converter import IRepresentationToModelConverter
from .representation_reader import IRepresentationReader
from src.domain.tasks_repository import TaskRepository
from src.services.markdown.markdown_parser import *

class MarkdownRepresentationReader(IRepresentationReader):
    def __init__(self, converter: IRepresentationToModelConverter) -> None:
        super().__init__()
        self.converter = converter

    def read(self, input: str) -> TaskRepository:
        parser = MarkdownParser()
        document = parser.parse(input)
        return self.converter.convert(document)