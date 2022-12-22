from tests.domain.domain_test_case import DomainTestCase
from src.domain.report_generator import Report, TaskRepository, WorkingDayRepository, RepositoryCollection
from src.services.domain.report_generation.burndown_graph_generator import BurndownGraphData, BurndownGraphGenerator

class GraphGeneratorTestCase(DomainTestCase):
    def test_empty_input_data(self):
        report = Report()
        task_repo = TaskRepository()
        holidays_repo = WorkingDayRepository()
        repositories = RepositoryCollection(task_repo, holidays_repo)

        graph_generator = BurndownGraphGenerator()

        graph_data = graph_generator.generate(report, repositories)

        self.assertIsInstance(graph_data, BurndownGraphData)