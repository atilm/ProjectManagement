from .domain_test_case import DomainTestCase
import datetime
from src.domain import weekdays
from src.domain.working_day_repository import WorkingDayRepository
from src.domain.report_generator import Report
from src.domain.free_range import FreeRange

class the_report_predicts_the_completion_date(DomainTestCase):
    def then_the_expected_completion_date_is(self, expectedDate: datetime.date , report: Report, projectId: str = ""):
        self.assertEqual(report.predicted_completion_dates[projectId].expected_value, expectedDate)

    def test_when_an_empty_repository_is_given(self):
        repo = self.given_an_empty_repository()

        report = self.when_a_report_is_generated(repo)

        # then no completion date is calculated
        self.assertEqual(report.predicted_completion_dates, {})
        # self.assertIsNone(report.predicted_completion_date)

    def test_predict_one_task_with_all_working_days(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(datetime.date(2022, 12, 5), 3, 6), #velocity of 0.5
            self.todo_task(2)
        ])

        report = self.when_a_report_is_generated(repo, datetime.date(2022, 12, 6))

        self.then_the_expected_completion_date_is(datetime.date(2022, 12, 10), report)

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
        self.then_the_expected_completion_date_is(datetime.date(2022, 12, 14), report)

    def test_skipping_free_ranges(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(datetime.date(2022, 12, 5), 3, 6), #velocity of 0.5
            self.todo_task(2),
            self.todo_task(2)
        ])

        workdays = WorkingDayRepository()
        workdays.set_free_weekdays(weekdays.SATURDAY, weekdays.SUNDAY)
        workdays.add_free_range(datetime.date(2022, 12, 12), datetime.date(2022, 12, 18)) # Mo to Su
        workdays.add_free_range(datetime.date(2022, 12, 26), datetime.date(2022, 12, 26)) # single free day: Mo

        thursday = datetime.date(2022, 12, 8)
        report = self.when_a_report_is_generated(repo, thursday, workdays)

        # then the completion date is after weekend and holidays
        self.then_the_expected_completion_date_is(datetime.date(2022, 12, 28), report)

    def test_start_date_is_not_a_working_day(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(datetime.date(2022, 12, 5), 3, 6), #velocity of 0.5
            self.todo_task(1)
        ])

        freeDay = datetime.date(2022, 12, 26)
        workdays = WorkingDayRepository()
        workdays.add_free_range(freeDay, freeDay) # single free day: Mo

        report = self.when_a_report_is_generated(repo, freeDay, workdays)

        self.then_the_expected_completion_date_is(datetime.date(2022, 12, 29), report)
    
    def test_work_amounts_to_a_fraction_of_a_day(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(datetime.date(2022, 12, 5), 8, 4), #velocity of 2
            self.todo_task(1) # -> half a day of work
        ])

        startDate = datetime.date(2022, 12, 8)
        report = self.when_a_report_is_generated(repo, startDate, WorkingDayRepository())

        # then the work is completed on the same day
        self.then_the_expected_completion_date_is(startDate, report)

    def test_fraction_of_day_must_be_completed_after_weekend(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(datetime.date(2022, 12, 5), 8, 4), #velocity of 2
            self.todo_task(3) # effort = 1.5 days
        ])

        freeWeekendsRepo = WorkingDayRepository()
        freeWeekendsRepo.set_free_weekdays(weekdays.SATURDAY, weekdays.SUNDAY)

        startDate = datetime.date(2023, 1, 13) # friday
        report = self.when_a_report_is_generated(repo, startDate, freeWeekendsRepo)

        self.then_the_expected_completion_date_is(datetime.date(2023, 1, 16), report)

    def test_completion_dates_are_reported_per_project(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(datetime.date(2022, 12, 5), 1, 1, "1"), #velocity of 1
            self.todo_task(1, "1"),
            self.todo_task(1, "1"),
            self.todo_task(1, "2"),
            self.todo_task(1, "2"),
            self.todo_task(1, "3"),
            self.todo_task(1, "3"),
        ])

        startDate = datetime.date(2023, 1, 1)
        report = self.when_a_report_is_generated(repo, startDate)

        self.then_the_expected_completion_date_is(startDate + datetime.timedelta(2), report, "1")
        self.then_the_expected_completion_date_is(startDate + datetime.timedelta(4), report, "2")
        self.then_the_expected_completion_date_is(startDate + datetime.timedelta(6), report, "3")

    def test_completion_date_is_calculated_correctly_with_two_working_day_repos(self):
        repo = self.given_a_repository_with_tasks([
            self.completed_task(datetime.date(2022, 12, 5), 8, 4), #velocity of 2
            self.todo_task(3),
            self.todo_task(5), # total effort: 4 days
        ])

        startDate = datetime.date(2023, 10, 16) # monday

        # Two developers with 3 holidays each and 1 day holiday overlap
        working_days_A = self.given_a_working_days_repository([weekdays.SATURDAY, weekdays.SUNDAY], [FreeRange(datetime.date(2023, 10, 17), datetime.date(2023, 10, 18), "holiday a")])
        working_days_B = self.given_a_working_days_repository([weekdays.SATURDAY, weekdays.SUNDAY], [FreeRange(datetime.date(2023, 10, 18), datetime.date(2023, 10, 19), "holiday b")])

        report = self.when_a_report_is_generated(repo, startDate, working_days_A, working_days_B)

        self.then_the_expected_completion_date_is(startDate + datetime.timedelta(8), report)
