from .representation_to_model_converter import IRepresentationToModelConverter
from .representation_reader import IRepresentationReader
from src.domain.repository_collection import RepositoryCollection
from src.services.markdown.markdown_parser import *

class MarkdownRepresentationReader(IRepresentationReader):
    def __init__(self, converter: IRepresentationToModelConverter) -> None:
        super().__init__()
        self.converter = converter

    def read(self, input: str) -> RepositoryCollection:
        parser = MarkdownParser()
        document = parser.parse(input)
        return self.converter.convert(document)