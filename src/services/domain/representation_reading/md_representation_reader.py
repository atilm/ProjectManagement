from .representation_reader import IRepresentationReader
from src.domain.tasks_repository import TaskRepository

class MarkdownRepresentationReader(IRepresentationReader):
    def read(source: str) -> TaskRepository:
        pass
        # convert source string to markdown document
        # convert markdown document to TaskRepository (different variants)
        # return repo