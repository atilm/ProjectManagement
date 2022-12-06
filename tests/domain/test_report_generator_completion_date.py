from .domain_test_case import DomainTestCase
import datetime
from src.domain import weekdays
from src.domain.working_day_repository import WorkingDayRepository

class the_report_predicts_the_completion_date(DomainTestCase):
    def test_when_an_empty_repository_is_given(self):
        repo = self.given_an_empty_repository()

        report = self.when_a_report_is_generated(repo)

        # then no completion date is calculated
        self.assertIsNone(report.predicted_completion_date)

    def test_predict_one_task_with_all_working_days(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(datetime.date(2022, 12, 5), 3, 6), #velocity of 0.5
            self.todo_task(2)
        ])

        report = self.when_a_report_is_generated(repo, datetime.date(2022, 12, 6))

        # then the predicted completion date is calculated
        self.assertEqual(report.predicted_completion_date, datetime.date(2022, 12, 10))

    def test_skipping_weekends(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(datetime.date(2022, 12, 5), 3, 6), #velocity of 0.5
            self.todo_task(2)
        ])

        workdays = WorkingDayRepository()
        workdays.set_free_weekdays(weekdays.SATURDAY, weekdays.SUNDAY)

        thursday = datetime.date(2022, 12, 8)
        report = self.when_a_report_is_generated(repo, thursday, workdays)

        # then the completion date is 4 days + 2 weekend days in the future
        self.assertEqual(report.predicted_completion_date, datetime.date(2022, 12, 14))

    def test_more_work_to_do(self):
        self.fail("more work to do")
    # specifying free ranges (holidays)
    # specifying free single days (holidays)
    # leap years ?
    # fractional workdays
    # today is not a working day
