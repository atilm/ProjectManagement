from .domain_test_case import DomainTestCase
from datetime import date
from src.domain.report_generator import *
from src.domain import weekdays

class the_report_predicts_completion_dates_per_story(DomainTestCase):
    def test_no_todo_tasks(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(date(2022,12,18), 1, 2) # velocity = 0.5
        ])

        report = self.when_a_report_is_generated(repo)

        self.assertEqual(report.task_completion_dates, [])

    def test_no_completed_tasks(self):
        repo = self.given_an_empty_repository()

        report = self.when_a_report_is_generated(repo)

        self.assertEqual(report.warnings, {"No velocity could be calculated."})

    def then_the_completion_dates_are(self, actualTasks: list, expectedDates: list):
        actualDates = [t.completedDate for t in actualTasks]
        self.assertEqual(actualDates, expectedDates)

    def test_one_todo_task(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(date(2022,12,18), 1, 2), # velocity = 0.5
            self.todo_task(2)
        ])

        report = self.when_a_report_is_generated(repo, date(2023, 1, 1))

        self.then_the_completion_dates_are(report.task_completion_dates, [date(2023,1,5)])

    def test_one_todo_task_taking_a_fractional_day(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(date(2022,12,18), 2, 1), # velocity = 2
            self.todo_task(1)
        ])

        startDate = date(2023, 1, 1)
        report = self.when_a_report_is_generated(repo, startDate)

        self.then_the_completion_dates_are(report.task_completion_dates, [startDate])

    def test_one_todo_task_taking_fractional_days_greater_than_1(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(date(2022,12,18), 2, 1), # velocity = 2
            self.todo_task(3)
        ])

        startDate = date(2023, 1, 1)
        report = self.when_a_report_is_generated(repo, startDate)

        self.then_the_completion_dates_are(report.task_completion_dates, [startDate + datetime.timedelta(1)])

    def test_two_todo_tasks_taking_integral_days(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(date(2022,12,18), 1, 1), # velocity = 1
            self.todo_task(1),
            self.todo_task(2) 
        ])

        startDate = date(2023, 1, 1)
        report = self.when_a_report_is_generated(repo, startDate)

        self.then_the_completion_dates_are(report.task_completion_dates, [
           date(2023, 1, 2),
           date(2023, 1, 4)
           ])

    def test_two_todo_tasks_taking_fractional_days(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(date(2022,12,18), 2, 1), # velocity = 2
            self.todo_task(3), # 1.5 days duration
            self.todo_task(3)  # 1.5 days duration
        ])

        startDate = date(2023, 1, 1)
        report = self.when_a_report_is_generated(repo, startDate)

        self.then_the_completion_dates_are(report.task_completion_dates, [
           date(2023, 1, 2),
           date(2023, 1, 4)
           ])

    def test_date_calculations_between_weekends_and_holidays(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(date(2022,12,18), 2, 1), # velocity = 2
            self.todo_task(3), # 1.5 days duration
            self.todo_task(3),
            self.todo_task(3),
        ])

        workingDaysRepo = WorkingDayRepository()
        workingDaysRepo.set_free_weekdays(weekdays.SATURDAY, weekdays.SUNDAY)
        workingDaysRepo.add_free_range(date(2022, 12, 26), date(2022, 12, 26))
        workingDaysRepo.add_free_range(date(2022, 12, 28), date(2022, 12, 29))

        startDate = date(2022, 12, 22)
        report = self.when_a_report_is_generated(repo, startDate, workingDaysRepo)

        self.then_the_completion_dates_are(report.task_completion_dates, [
           date(2022, 12, 23),
           date(2022, 12, 28),
           date(2023, 1, 2),
           ])
