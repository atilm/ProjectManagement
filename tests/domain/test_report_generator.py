from .domain_test_case import DomainTestCase
from src.domain.report_generator import *
from src.domain.task import *
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
    def create_task(self, completedDate: datetime.date, estimate: float, actualWorkDays: float) -> Task:
        task = Task(self._id_generator.next(), "")
        task.estimate = estimate
        task.actualWorkDays = actualWorkDays
        task.completedDate = completedDate
        task.startedDate = completedDate - datetime.timedelta(actualWorkDays) if actualWorkDays is not None else completedDate
        task.createdDate = task.startedDate
        return task

    def test_calculate_velocity_from_a_single_task(self):
        task = self.create_task(datetime.date(2022, 12, 4), 3, 5.5)
        repo = self.given_a_repository_with_tasks([task])

        report = self.when_a_report_is_generated(repo)

        # then the velocity is calculated from this task
        self.assertAlmostEqual(report.velocity, 0.55, places=2)

    def test_calculate_velocity_from_two_tasks(self):
        repo = self.given_a_repository_with_tasks([
            self.create_task(datetime.date(2022, 12, 4), 3, 5.5),
            self.create_task(datetime.date(2022, 12, 4), 5, 8.0)
        ])

        report = self.when_a_report_is_generated(repo)

        # then the velocity is the arithmetic mean of the two single velocities
        self.assertAlmostEqual(report.velocity, 0.59, places=2)

    def test_duration_of_zero(self):
        task = self.create_task(datetime.date(2022, 12, 4), 3, 0.0)
        repo = self.given_a_repository_with_tasks([task])

        exception = self.then_report_generation_raises(repo)

        self.assertIsInstance(exception, VelocityCalculationException)
        self.assertEqual(exception.task_id, task.id)

    def test_tasks_without_estimate_are_ignored(self):
        repo = self.given_a_repository_with_tasks([
            self.create_task(datetime.date(2022, 12, 4), None, 1.0)
        ])

        report = self.when_a_report_is_generated(repo)

        # then no velocity is calculated
        self.assertIsNone(report.velocity)

    def test_tasks_without_actual_work_days_are_ignored(self):
        repo = self.given_a_repository_with_tasks([
            self.create_task(datetime.date(2022, 12, 4), 3, None)
        ])

        report = self.when_a_report_is_generated(repo)

        # then no velocity is calculated
        self.assertIsNone(report.velocity)

    def test_removed_tasks_are_ignored(self):
        task = self.create_task(datetime.date(2022, 12, 4), 3, 1)
        task.removedDate = datetime.date(2022, 12, 4)
        repo = self.given_a_repository_with_tasks([
            task
        ])

        report = self.when_a_report_is_generated(repo)

        # then no velocity is calculated
        self.assertIsNone(report.velocity)

    def test_only_the_30_most_recent_tasks_are_used(self):
        startDate = datetime.date(2022, 2, 1)
        tasks = [self.create_task(startDate + datetime.timedelta(i), 1, 1) for i in range(29)]
        tasks.append(self.create_task(startDate + datetime.timedelta(30), 1, 0.01))
        tasks.append(self.create_task(startDate - datetime.timedelta(1), 1, 0.001))

        repo = self.given_a_repository_with_tasks(tasks)

        report = self.when_a_report_is_generated(repo)

        # then the velocity is (29 * 1 + 100) / 30
        self.assertAlmostEqual(report.velocity, 4.3, places=2)
