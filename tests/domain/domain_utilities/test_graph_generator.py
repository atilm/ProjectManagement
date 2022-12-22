import datetime
from tests.domain.domain_test_case import DomainTestCase
from src.domain.report_generator import Report, TaskRepository, WorkingDayRepository, RepositoryCollection, TaskReport
from src.services.domain.report_generation.burndown_graph_generator import XyData, BurndownGraphGenerator, BurndownGraphData, FreeRange
from src.domain import weekdays

def get_comp_date(report: Report, index, attr):
    completion_date = report.task_reports[index].completion_date
    return getattr(completion_date, attr)

class GraphGeneratorTestCase(DomainTestCase):
    def assert_xy_data(self, xy_data: XyData, expected_x: list, expected_y: list):
        self.assertEqual(xy_data.x, expected_x)
        self.assertEqual(xy_data.y, expected_y)


    def given_a_report(self, taskReports: list = []):
        report = Report()
        report.task_reports = taskReports
        return report
        
    def when_graph_data_are_generated(self, report: Report, task_repo, holidays_repo) -> BurndownGraphData:
        graph_generator = BurndownGraphGenerator()
        repositories = RepositoryCollection(task_repo, holidays_repo)
        return graph_generator.generate(report, repositories)

    def test_empty_input_data(self):
        graph_data = self.when_graph_data_are_generated(Report(), TaskRepository(), WorkingDayRepository())

        self.assert_xy_data(graph_data.lower_confidence_band, [], [])
        self.assert_xy_data(graph_data.expected_values, [], [])
        self.assert_xy_data(graph_data.upper_confidence_band, [], [])
        self.assertEqual(graph_data.free_date_ranges, [])

    def test_free_date_ranges_contains_only_holidays(self):
        expected_free_ranges = [FreeRange(datetime.date(2022, 12, 22), datetime.date(2022, 12, 22), "")]

        holidays_repo = self.given_a_working_days_repository(
            [weekdays.SATURDAY, weekdays.SUNDAY],
            expected_free_ranges)
        report = self.given_a_report()

        graph_data = self.when_graph_data_are_generated(report, TaskRepository(), holidays_repo)

        self.assertEqual(graph_data.free_date_ranges, expected_free_ranges)

    def test_graph_data_contains_sorted_series_of_completed_and_todo_tasks(self):
        first_todo = self.todo_task(2)
        second_todo = self.todo_task(3)

        task_repo = self.given_a_repository_with_tasks([
            self.completed_task(datetime.date(2022, 12, 8), 2, 4),
            self.completed_task(datetime.date(2022, 12, 4), 5, 10),
            first_todo,
            second_todo
        ])

        holidays_repo = WorkingDayRepository()

        report = self.when_a_report_is_generated(task_repo, datetime.date(2022, 12, 8), holidays_repo)

        graph_data = self.when_graph_data_are_generated(report, task_repo, holidays_repo)

        remaining_effort = [7, 5, 3, 0]
        expected_completion_dates = [
            datetime.date(2022, 12, 4), datetime.date(2022, 12, 8), get_comp_date(report, 0, "expected_value"), get_comp_date(report, 1, "expected_value")
        ]
        lower_limit_dates = [
            datetime.date(2022, 12, 4), datetime.date(2022, 12, 8), get_comp_date(report, 0, "lower_limit"), get_comp_date(report, 1, "lower_limit")
        ]
        uppper_limit_dates = [
            datetime.date(2022, 12, 4), datetime.date(2022, 12, 8), get_comp_date(report, 0, "upper_limit"), get_comp_date(report, 1, "upper_limit")
        ]

        self.assert_xy_data(graph_data.expected_values,
            expected_completion_dates,
            remaining_effort)

        self.assert_xy_data(graph_data.lower_confidence_band,
            lower_limit_dates,
            remaining_effort)

        self.assert_xy_data(graph_data.upper_confidence_band,
            uppper_limit_dates,
            remaining_effort)

        

