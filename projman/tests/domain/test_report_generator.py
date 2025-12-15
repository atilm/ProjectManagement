from .domain_test_case import DomainTestCase
from projman.src.domain.report_generator import *
from projman.src.domain.task import *
import datetime

class the_user_can_generate_a_report_from_a_task_repository(DomainTestCase):
    def test_generation_from_an_empty_repository(self):
        repo = self.given_an_empty_repository()
        
        report = self.when_a_report_is_generated(repo)

        # then a report is returned
        self.assertIsInstance(report, Report)

        # then the velocity is none
        self.assertIsNone(report.velocity)

class the_report_contains_the_velocity_from_the_30_most_recent_tasks(DomainTestCase):
    def test_calculate_velocity_from_a_single_task(self):
        task = self.completed_task(datetime.date(2022, 12, 4), 3, 5)
        repo = self.given_a_repository_with_tasks([task])

        report = self.when_a_report_is_generated(repo)

        # then the velocity is calculated from this task
        self.assertAlmostEqual(report.velocity, 0.6, places=2)

    def test_calculate_velocity_from_two_tasks(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(datetime.date(2022, 12, 5), 3, 5.0),
            self.completed_task(datetime.date(2022, 12, 4), 5, 8.0)
        ])

        report = self.when_a_report_is_generated(repo)

        # then the velocity is (3 + 5) / 9
        # beause global start-date is 2022-12-4 - 8 days and global completed date is 2022-12-5
        self.assertAlmostEqual(report.velocity, 0.88888, places=4)

    def test_duration_of_zero(self):
        task = self.completed_task(datetime.date(2022, 12, 4), 3, 0.0)
        repo = self.given_a_repository_with_tasks([task])

        exception = self.then_report_generation_raises(repo)

        self.assertIsInstance(exception, VelocityCalculationException)
        self.assertEqual(exception.task_id, -1) # because in general several tasks could be involved

    def test_tasks_without_estimate_are_ignored(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(datetime.date(2022, 12, 4), None, 1.0)
        ])

        report = self.when_a_report_is_generated(repo)

        # then no velocity is calculated
        self.assertIsNone(report.velocity)

    def test_tasks_without_start_date_are_ignored(self):
        taskWithoutStartDate = self.completed_task(datetime.date(2022, 12, 4), 3, None)
        taskWithoutStartDate.startedDate = None

        repo = self.given_a_repository_with_tasks([
            taskWithoutStartDate
        ])

        report = self.when_a_report_is_generated(repo)

        # then no velocity is calculated
        self.assertIsNone(report.velocity)

    def test_removed_tasks_are_ignored(self):
        task = self.completed_task(datetime.date(2022, 12, 4), 3, 1)
        task.removedDate = datetime.date(2022, 12, 4)
        repo = self.given_a_repository_with_tasks([
            task
        ])

        report = self.when_a_report_is_generated(repo)

        # then no velocity is calculated
        self.assertIsNone(report.velocity)

    def test_only_the_30_most_recent_tasks_are_used(self):
        startDate = datetime.date(2022, 2, 2)
        tasks = [self.completed_task(startDate + datetime.timedelta(i), 1, 1) for i in range(29)]
        tasks.append(self.completed_task(startDate + datetime.timedelta(30), 5, 1))
        
        tasks.append(self.completed_task(startDate - datetime.timedelta(1), 21, 1))

        repo = self.given_a_repository_with_tasks(tasks)

        report = self.when_a_report_is_generated(repo)

        # global start date: 2022-2-2 - 1 day, because one earlier date is ignored
        # global completed date: 2022-2-2 + 30 days
        # velocity: (29 + 5) story points / 31 days
        self.assertAlmostEqual(report.velocity, 1.09677, places=4)

class the_report_contains_the_sum_of_remaining_estimated_workdays_todo(DomainTestCase):
    def test_when_no_tasks_are_given_0_is_returned(self):
        repo = self.given_an_empty_repository()

        report = self.when_a_report_is_generated(repo)

        # then the remaining workdays are 0
        self.assertEqual(report.remaining_work_days.expected_value, 0)

    def test_when_only_a_completed_task_is_given_0_is_returned(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(datetime.date(2022, 3, 3), 1, 1)
        ])

        report = self.when_a_report_is_generated(repo)

        # then the remaining workdays are 0
        self.assertEqual(report.remaining_work_days.expected_value, 0)

    def test_when_a_completed_and_an_estimated_todo_task_are_given(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(datetime.date(2022, 1, 1), 3, 6),
            self.todo_task(5)
        ])

        report = self.when_a_report_is_generated(repo)

        # then the remaining days are calculated
        self.assertAlmostEqual(report.remaining_work_days.expected_value, 10, places=2)

    def test_when_a_completed_and_two_estimated_tasks_are_given(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(datetime.date(2022, 1, 1), 3, 6, "project1"),
            self.todo_task(5,  "project1"),
            self.todo_task(3,  "project1")
        ])

        report = self.when_a_report_is_generated(repo)

        # then the sum of the durations is returned
        self.assertAlmostEqual(report.remaining_work_days.expected_value, 16, places=2)
        self.assertEqual(report.predicted_completion_dates["project1"].expected_value, datetime.date(2022, 1, 17))

    def test_when_a_completed_and_some_estimated_and_some_unestimated_tasks_are_given(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(datetime.date(2022, 1, 1), 3, 6),
            self.todo_task(5),
            self.todo_task(8),
            self.todo_task(None)
        ])

        report = self.when_a_report_is_generated(repo)

        # then the sum of the durations is returned
        self.assertAlmostEqual(report.remaining_work_days.expected_value, 26, places=2)

        # then the report contains a warning about unestimated tasks
        # self.assertEqual(report.warnings, {"Unestimated stories have been ignored."})
        self.assertEqual(report.warnings, {"Unestimated stories have been ignored."})
