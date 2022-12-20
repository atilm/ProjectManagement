from datetime import date
from .domain_test_case import DomainTestCase
from src.domain.report_generator import *

class the_report_generator_calculates_completion_date_ranges(DomainTestCase):
    def test_a_report_contains_confidence_intervals_for_predicitions(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(date(2022,12,18), 1, 2), # velocity = 0.5
            self.todo_task(2) # estimate: (1,2,3) -> (2d, 4d, 6d)
        ])

        report = self.when_a_report_is_generated(repo, date(2023, 1, 1))

        taskReport: TaskReport = report.task_reports[0]
        self.assertIsInstance(report.predicted_completion_date, ConfidenceInterval)
        #self.assertIsInstance(taskReport.completion_date, ConfidenceInterval)

        self.assertEqual(taskReport.estimated_days, ConfidenceInterval(2, 4, 6))
        self.assertEqual(taskReport.completion_date, ConfidenceInterval(date(2023, 1, 3), date(2023, 1, 5), date(2023, 1, 7)))

        