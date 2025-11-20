from datetime import date
from .domain_test_case import DomainTestCase
from projman.src.domain.report_generator import *
from math import *

class the_report_generator_calculates_completion_date_ranges(DomainTestCase):
    def test_a_report_contains_confidence_intervals_for_predicitions(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(date(2022,12,18), 1, 2), # velocity = 0.5
            self.todo_task(2) # estimate: (1,2,3) -> (2d, 4d, 6d)
        ])

        report = self.when_a_report_is_generated(repo, date(2023, 1, 1))

        taskReport: TaskReport = report.task_reports[0]
        expected_completion_date_interval = ConfidenceInterval(date(2023, 1, 3), date(2023, 1, 5), date(2023, 1, 7))
        self.assertEqual(taskReport.estimated_days, ConfidenceInterval(2, 4, 6))
        self.assertEqual(taskReport.completion_date, expected_completion_date_interval)
        self.assertEqual(report.remaining_work_days, ConfidenceInterval(2, 4, 6))
        self.assertEqual(report.predicted_completion_dates[""], expected_completion_date_interval)


    def test_estimation_errors_are_combined_as_sums_of_squares(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(date(2022,12,18), 1, 2), # velocity = 0.5
            self.todo_task(3), # estimate: (2,3,5) -> (4d, 6d, 10d) -> 6d -2d / +4d
            self.todo_task(8), # estimate: (5,8,13) -> (10d, 16d, 26d) -> 16d -6d / + 10d
        ])

        startDate = date(2023, 1, 1)

        first_expected_interval = ConfidenceInterval(date(2023, 1, 5), date(2023, 1, 7), date(2023, 1, 11))
        # estimation errors of subsequent tasks should add in a "squared" manner
        second_expected_interval = ConfidenceInterval(
            startDate + datetime.timedelta(22 - sqrt(2**2 + 6**2)),
            startDate + datetime.timedelta(22),
            startDate + datetime.timedelta(22 + sqrt(4**2 + 10**2))
        )

        report = self.when_a_report_is_generated(repo, startDate)

        actual_intervals = [tr.completion_date for tr in report.task_reports]
        self.assertEqual(actual_intervals, [first_expected_interval, second_expected_interval])

    def test_exception_when_estimate_is_not_a_fibonacci_number(self):
        self._assert_exception_on_estimate(4)
        self._assert_exception_on_estimate(55)

    def _assert_exception_on_estimate(self, estimate):
        todo_task = self.todo_task(estimate)

        repo = self.given_a_repository_with_tasks([
            self.completed_task(date(2022,12,18), 1, 2),
            todo_task,
        ])

        error = self.then_report_generation_raises(repo)

        self.assertIsInstance(error, NotAFibonacciEstimateException, f"Estimate: {estimate}")
        self.assertEqual(error.task_id, todo_task.id)
        
    def test_stories_with_estimate_0_are_filtered_out(self):
        todo_task = self.todo_task(0)

        repo = self.given_a_repository_with_tasks([
            self.completed_task(date(2022,12,18), 1, 2),
            todo_task,
        ])

        report = self.when_a_report_is_generated(repo)

        self.assertEqual(len(report.task_reports), 0)
