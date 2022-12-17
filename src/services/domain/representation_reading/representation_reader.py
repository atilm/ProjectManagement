from src.domain.repository_collection import RepositoryCollection

class IRepresentationReader:
    """This is the controller class which will coordinate
    the steps to get data from a data source (e.g. read from file) 
    and convert them into the domain model"""
    def read(self, source: object) -> RepositoryCollection:
        pass