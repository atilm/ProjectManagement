from datetime import date
from .domain_test_case import DomainTestCase
from src.domain.report_generator import *

class the_report_generator_calculates_completion_date_ranges(DomainTestCase):
    def test_a_report_contains_confidence_intervals_for_predicitions(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(date(2022,12,18), 1, 2),
            self.todo_task(2)
        ])

        report = self.when_a_report_is_generated(repo, date(2023, 1, 1))

        taskReport: TaskReport = report.task_reports[0]
        self.assertIsInstance(report.predicted_completion_date, ConfidenceInterval)
        self.assertIsInstance(taskReport.completion_date, ConfidenceInterval)
        self.assertIsInstance(taskReport.estimated_days, ConfidenceInterval)
        