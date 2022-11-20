from .representation_reader import IRepresentationReader
from src.domain.tasks_repository import TaskRepository

class MarkdownRepresentationReader(IRepresentationReader):
    def read(source: str) -> TaskRepository:
        pass
        # read file to string
        # convert string to markdown document
        # convert markdown document to TaskRepository (different variants)
        # return repo