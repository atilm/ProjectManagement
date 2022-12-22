from src.domain.report_generator import Report
from src.domain.repository_collection import RepositoryCollection

class BurndownGraphData:
    """docstring"""
    pass

class BurndownGraphGenerator:
    """Generates data containing information for a burndown chart.
    This data must be passed to a GraphEngine"""
    def generate(self, report: Report, repositories: RepositoryCollection) -> BurndownGraphData:
        return BurndownGraphData()