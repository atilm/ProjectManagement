from .representation_to_model_converter import IRepresentationToModelConverter
from .representation_reader import IRepresentationReader
from src.domain.repository_collection import RepositoryCollection, TaskRepository, WorkingDayRepositoryCollection, mergeRepos
from src.services.markdown.markdown_parser import *
from typing import List

class MarkdownMultiRepresentationReader(IRepresentationReader):
    def __init__(self, converter: IRepresentationToModelConverter) -> None:
        super().__init__()
        self.converter = converter

    def read(self, input_strings: List[str]) -> RepositoryCollection:
        parser = MarkdownParser()

        repos_collection = RepositoryCollection(TaskRepository(), WorkingDayRepositoryCollection())

        for s in input_strings:
            document = parser.parse(s)
            repos_from_string = self.converter.convert(document)
            repos_collection = mergeRepos(repos_collection, repos_from_string)

        return repos_collection