from src.domain.repository_collection import RepositoryCollection

class IRepresentationWriter:
    def write(self, repos: RepositoryCollection) -> object:
        pass