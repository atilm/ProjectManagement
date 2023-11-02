import datetime
from tests.services.test_graph_generator import GraphGeneratorTestCase
from src.domain.completion_date_history import CompletionDateHistory
from src.domain.report_generator import ConfidenceInterval
from src.services.domain.graph_generation.project_tracking_graph_generator import ProjectTrackingGraphGenerator

def day(dayInMonth: int) -> datetime.date:
        return datetime.date(2023, 11, dayInMonth)

class TrackingGraphGeneratorTests(GraphGeneratorTestCase):

    def test_generate_graph_data_from_a_valid_data_structure(self):
        history = CompletionDateHistory("project-id")
        history.add(day(2), ConfidenceInterval(day(12), day(17), day(28)))
        history.add(day(4), ConfidenceInterval(day(16), day(18), day(21)))

        generator = ProjectTrackingGraphGenerator()
        graph_data = generator.generate(history)

        self.assertEqual(graph_data.title, "Project: project-id")
        self.assert_xy_data(graph_data.lower_confidence_band, [day(2), day(4)], [day(12), day(16)])
        self.assert_xy_data(graph_data.expected_values, [day(2), day(4)], [day(17), day(18)])
        self.assert_xy_data(graph_data.upper_confidence_band, [day(2), day(4)], [day(28), day(21)])
