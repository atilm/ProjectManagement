from tests.domain.domain_test_case import DomainTestCase
from src.services.domain.graph_generation.estimation_error_graph_generator import *
import datetime
from src.global_settings import GlobalSettings

class EstimationErrorGraphGeneratorTestCase(DomainTestCase):
    def when_graph_data_are_generated(self, repo: TaskRepository) -> EstimationErrorGraphData:
        generator = EstimationErrorGraphGenerator()
        return generator.generate(repo)

    def then_the_relative_errors_are(self, estimates: list, relative_errors: list, data: EstimationErrorGraphData):
        for actual, expected in zip(relative_errors, data.relative_errors.x):
            self.assertAlmostEqual(actual, expected)

        self.assertEqual(data.relative_errors.y, estimates)

    def then_warnings_are_pressent(self, expectedWarnings: list, data: EstimationErrorGraphData):
        self.assertEqual(data.warnings, expectedWarnings)

    def test_empty_input_data(self):
        repo = self.given_an_empty_repository()

        data = self.when_graph_data_are_generated(repo)

        self.assertIsInstance(data, EstimationErrorGraphData)
        self.then_the_relative_errors_are([], [], data)

    def test_errors_are_calculated(self):
        # taskWithoutEstimateAtBeginning = self.completed_task(datetime.date(2023, 1, 1), None, 1)
        taskWithoutDurationAtEnd = self.completed_task(datetime.date(2023, 1, 14), 1, None)
        taskWithoutEstimateAtEnd = self.completed_task(datetime.date(2023, 1, 15), None, 1)

        repo = self.given_a_repository_with_tasks([
            # taskWithoutEstimateAtBeginning,
            self.completed_task(datetime.date(2023, 1, 6), 2, 1),
            self.completed_task(datetime.date(2023, 1, 12), 5, 1.2), # input not sorted by completion date!
            self.completed_task(datetime.date(2023, 1, 7), 8, 1),
            taskWithoutDurationAtEnd,
            taskWithoutEstimateAtEnd,
        ])

        data = self.when_graph_data_are_generated(repo)

        self.then_the_relative_errors_are([8, 5], [-0.75, 0.2], data)
        self.then_warnings_are_pressent({
            # f"Story {taskWithoutEstimateAtBeginning.id} has no estimate or workdays and was ignored.",
            f"Story {taskWithoutDurationAtEnd.id} has no estimate or workdays and was ignored.",
            f"Story {taskWithoutEstimateAtEnd.id} has no estimate or workdays and was ignored.",
        }, data)

