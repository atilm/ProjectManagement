from src.domain.repository_collection import RepositoryCollection

class IRepresentationToModelConverter:
    """This is the to convert a data source's in-memory-representation
    into the domain model"""
    def convert(self, source : object) -> RepositoryCollection:
        pass