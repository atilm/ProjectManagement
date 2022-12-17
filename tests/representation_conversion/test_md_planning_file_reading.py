import unittest
from datetime import date, timedelta
from src.services.domain.representation_reading.md_planning_file_to_model_converter import *
from src.services.markdown.markdown_document_builder import *
from src.domain.task import Task
from tests.domain.domain_utilities.task_utilities import *
from src.domain.working_day_repository import WorkingDayRepository

correctTableHeader = ["Id", "Description", "Estimate", "Started", "Completed", "Workdays", "Created", "Removed"]

class MarkdownPlanningDocumentToModelConverterTestCase(unittest.TestCase):
    def given_a_document_with_tables(self, todo: MarkdownTable, completed: MarkdownTable, removed: MarkdownTable) -> MarkdownDocument:
        return self.build_table(self.build_default_working_days_table(), self.build_empty_holidays_table(), todo, completed, removed)

    def given_a_document_with_holidays(self, workingDays, holidays) -> MarkdownDocument:
        todo = self.build_empty_table()
        completed = self.build_empty_table()
        removed = self.build_empty_table()
        return self.build_table(workingDays, holidays, todo, completed, removed)

    def build_table(self, workingDays, holidays, todo, completed, removed) -> MarkdownDocument:
        return MarkdownDocumentBuilder()\
            .withSection("Planning", 0)\
            .withSection("Working Days", 1)\
            .withTable(workingDays)\
            .withSection("Holidays", 1)\
            .withTable(holidays)\
            .withSection("Stories To Do", 1)\
            .withTable(todo)\
            .withSection("Completed Stories", 1)\
            .withTable(completed)\
            .withSection("Removed Stories", 1)\
            .withTable(removed)\
            .build()

    def build_empty_table(self):
        return MarkdownTableBuilder()\
            .withHeader(*correctTableHeader)\
            .build()

    def build_default_working_days_table(self) -> MarkdownTable:
        return self.build_working_days_table(["x"] * 7)

    def build_working_days_table(self, row: list) -> MarkdownTable:
        return MarkdownTableBuilder()\
            .withHeader("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")\
            .withRow(*row)\
            .build()

    def build_empty_holidays_table(self) -> MarkdownTable:
        return self.build_holidays_table([])

    def build_holidays_table(self, holidayRows: list) -> MarkdownTable:
        builder = MarkdownTableBuilder().withHeader("Dates", "Description")

        for fields in holidayRows:
            builder.withRow(*fields)

        return builder.build()

    def when_the_document_is_converted(self, document: MarkdownDocument) -> TaskRepository:
        converter = MarkdownPlanningDocumentToModelConverter()
        repoCollection = converter.convert(document)
        return repoCollection.task_repository

    def when_the_document_is_converted_to_a_working_days_repo(self, document: MarkdownDocument) -> WorkingDayRepository:
        converter = MarkdownPlanningDocumentToModelConverter()
        repoCollection = converter.convert(document)
        return repoCollection.working_days_repository

    def then_the_repo_contains_id(self, taskId: str, repo: TaskRepository):
        task = repo.get(taskId)
        self.assertEqual(task.id, taskId)

    def then_the_repo_contains_task(self, task: Task, repo: TaskRepository):
        actualTask = repo.get(task.id)
        lhs = actualTask
        rhs = task
        self.assertEqual(lhs.id, rhs.id)
        self.assertEqual(lhs.description, rhs.description)
        self.assertTrue(isNumberOrNone(lhs.estimate))
        self.assertEqual(lhs.estimate, rhs.estimate)
        self.assertTrue(isDateOrNone(lhs.startedDate))
        self.assertEqual(lhs.startedDate, rhs.startedDate)
        self.assertTrue(isDateOrNone(lhs.completedDate))
        self.assertEqual(lhs.completedDate, rhs.completedDate)
        self.assertTrue(isNumberOrNone(lhs.actualWorkDays))
        self.assertEqual(lhs.actualWorkDays, rhs.actualWorkDays)
        self.assertTrue(isDateOrNone(lhs.createdDate))
        self.assertEqual(lhs.createdDate, rhs.createdDate)
        self.assertTrue(isDateOrNone(lhs.removedDate))
        self.assertEqual(lhs.removedDate, rhs.removedDate)

    def then_the_repo_contains_holidays(self, repo: WorkingDayRepository, firstFreeDay: date, lastFreeDay: date) -> None:
        self.assertFalse(repo.is_working_day(firstFreeDay))
        self.assertFalse(repo.is_working_day(lastFreeDay))

    def expect_conversion_exception(self, document: MarkdownDocument):
        try:
            self.when_the_document_is_converted(document)
        except Exception as e:
            return e
        
        self.fail("document conversion did not raise an exception")

    def then_the_exception_is(self, e : Exception, expectedType, lineNumber: int):
        self.assertIsInstance(e, expectedType)
        self.assertEqual(e.lineNumber, lineNumber)

class reading_tests(MarkdownPlanningDocumentToModelConverterTestCase):
    def test_the_converter_returns_a_repository(self):
        todo = self.build_empty_table()
        completed = self.build_empty_table()
        removed = self.build_empty_table()

        document = self.given_a_document_with_tables(todo, completed, removed)

        repo = self.when_the_document_is_converted(document)

        self.assertIsInstance(repo, TaskRepository)
        self.assertEqual(len(repo.tasks.items()), 0)

    def test_can_read_two_tasks_from_completed_table(self):
        todo = self.build_empty_table()
        completed = MarkdownTableBuilder()\
            .withHeader(*correctTableHeader)\
            .withRow("1", "Description 1", "3", "01-02-2020", "03-02-2020", "2", "29-01-2020", "")\
            .withRow("2", "Description 2", "5", "01-02-2021", "04-02-2021", "3.5", "29-01-2021", "")\
            .build()
        removed = self.build_empty_table()

        document = self.given_a_document_with_tables(todo, completed, removed)

        repo = self.when_the_document_is_converted(document)

        expectedTask1 = Task("1", "Description 1")
        expectedTask1.estimate = 3
        expectedTask1.startedDate = date(2020, 2, 1)
        expectedTask1.completedDate = date(2020, 2, 3)
        expectedTask1.actualWorkDays = 2
        expectedTask1.createdDate = date(2020, 1, 29)
        expectedTask1.removedDate = None

        expectedTask2 = Task("2", "Description 2")
        expectedTask2.estimate = 5
        expectedTask2.startedDate = date(2021, 2, 1)
        expectedTask2.completedDate = date(2021, 2, 4)
        expectedTask2.actualWorkDays = 3.5
        expectedTask2.createdDate = date(2021, 1, 29)
        expectedTask2.removedDate = None

        self.then_the_repo_contains_task(expectedTask1, repo)
        self.then_the_repo_contains_task(expectedTask2, repo)

    def test_can_read_a_task_from_to_do_table(self):
        todo = MarkdownTableBuilder()\
            .withHeader(*correctTableHeader)\
            .withRow("1", "Description", "5", "", "", "", "29-01-2021", "")\
            .build()
        completed = self.build_empty_table()
        removed = self.build_empty_table()

        document = self.given_a_document_with_tables(todo, completed, removed)

        repo = self.when_the_document_is_converted(document)

        expectedTask = Task("1", "Description")
        expectedTask.estimate = 5
        expectedTask.startedDate = None
        expectedTask.completedDate = None
        expectedTask.actualWorkDays = None
        expectedTask.createdDate = date(2021, 1, 29)
        expectedTask.removedDate = None

        self.then_the_repo_contains_task(expectedTask, repo)

    def test_can_read_a_task_from_removed_table(self):
        todo = self.build_empty_table()
        completed = self.build_empty_table()
        removed = MarkdownTableBuilder()\
            .withHeader(*correctTableHeader)\
            .withRow("3", "Description", "5", "04-05-2022", "", "", "01-05-2022", "05-05-2022")\
            .build()

        document = self.given_a_document_with_tables(todo, completed, removed)

        repo = self.when_the_document_is_converted(document)

        expectedTask = Task("3", "Description")
        expectedTask.estimate = 5
        expectedTask.startedDate = date(2022, 5, 4)
        expectedTask.completedDate = None
        expectedTask.actualWorkDays = None
        expectedTask.createdDate = date(2022, 5, 1)
        expectedTask.removedDate = date(2022, 5, 5)

        self.then_the_repo_contains_task(expectedTask, repo)

    def test_exception_on_unexpected_table_header(self):
        todo = self.build_empty_table()
        completed = self.build_empty_table()
        removed = MarkdownTableBuilder()\
            .withHeader("Id", "Description", "Started", "Completed", "Workdays", "Created", "Removed")\
            .build()
        removed._headerRow.lineNumber = 13

        document = self.given_a_document_with_tables(todo, completed, removed)

        e = self.expect_conversion_exception(document)

        self.then_the_exception_is(e, HeaderFormatException, 13)

    def test_exception_on_wrong_number_of_row_entries(self):
        todo = self.build_empty_table()
        completed = self.build_empty_table()
        removed = MarkdownTableBuilder()\
            .withHeader(*correctTableHeader)\
            .withRow("3", "Description", "5", "04-05-2022", "", "01-05-2022", "05-05-2022")\
            .build()

        removed.rows[0].lineNumber = 5

        document = self.given_a_document_with_tables(todo, completed, removed)

        e = self.expect_conversion_exception(document)

        self.then_the_exception_is(e, ColumnNumberException, 5)

    def test_exception_on_wrong_date_format(self):
        todo = self.build_empty_table()
        completed = self.build_empty_table()
        removed = MarkdownTableBuilder()\
            .withHeader(*correctTableHeader)\
            .withRow("3", "Description", "5", "12-31-2022", "", "", "01-05-2022", "05-05-2022")\
            .build()
        
        removed.rows[0].lineNumber = 5

        document = self.given_a_document_with_tables(todo, completed, removed)

        e = self.expect_conversion_exception(document)

        self.then_the_exception_is(e, ValueConversionException, 5)
        e.inputString = "12-31-2022"

    def test_weekly_working_days_are_parsed(self):
        workingDays = self.build_working_days_table(["", "a", "", "n", "", "y", ""])
        holidays = self.build_empty_holidays_table()
        document = self.given_a_document_with_holidays(workingDays, holidays)

        repo = self.when_the_document_is_converted_to_a_working_days_repo(document)

        monday = date(2022, 12, 12)
        aWeek = [monday + timedelta(d) for d in range(7)]

        self.assertFalse(repo.is_working_day(aWeek[MONDAY]))
        self.assertTrue(repo.is_working_day(aWeek[TUESDAY]))
        self.assertFalse(repo.is_working_day(aWeek[WEDNESDAY]))
        self.assertTrue(repo.is_working_day(aWeek[THURSDAY]))
        self.assertFalse(repo.is_working_day(aWeek[FRIDAY]))
        self.assertTrue(repo.is_working_day(aWeek[SATURDAY]))
        self.assertFalse(repo.is_working_day(aWeek[SUNDAY]))

    def test_exception_on_wrong_working_days_row_format(self):
        workingDays = self.build_working_days_table(["x", "x", "x"]) # too few columns
        workingDays.rows[0].lineNumber = 7
        holidays = self.build_empty_holidays_table()
        document = self.given_a_document_with_holidays(workingDays, holidays)

        e = self.expect_conversion_exception(document)

        self.then_the_exception_is(e, ColumnNumberException, 7)

    def test_exception_on_missing_working_days_row(self):
        workingDays = self.build_working_days_table([])
        workingDays._headerRow.lineNumber = 4
        workingDays.rows = []

        holidays = self.build_empty_holidays_table()
        document = self.given_a_document_with_holidays(workingDays, holidays)

        e = self.expect_conversion_exception(document)

        self.then_the_exception_is(e, MissingTableRowException, 6)

    def test_parse_a_single_holiday(self):
        holidays = self.build_holidays_table([(" 24-12-2022 ", " Christmas ")])
        workingDays = self.build_default_working_days_table()
        document = self.given_a_document_with_holidays(workingDays, holidays)

        repo = self.when_the_document_is_converted_to_a_working_days_repo(document)

        holidays: FreeRange = repo.free_ranges[0]
        self.assertFalse(repo.is_working_day(date(2022, 12, 24)))
        self.assertEqual(holidays.description, "Christmas")

    def test_parse_holidays(self):
        holidays = self.build_holidays_table([
            ("02-01-2023 -- 06-01-2023 ", " Skiing "),
            (" 24-12-2022 ", " Christmas ")])
        workingDays = self.build_default_working_days_table()
        document = self.given_a_document_with_holidays(workingDays, holidays)

        repo = self.when_the_document_is_converted_to_a_working_days_repo(document)
        
        self.then_the_repo_contains_holidays(repo, date(2023, 1, 2), date(2023, 1, 6))
        self.then_the_repo_contains_holidays(repo, date(2022, 12, 24), date(2022, 12, 24))

    def test_holiday_row_with_wrong_format(self):
        holidays = self.build_holidays_table([
            (" 24-12-2022 ")])
        holidays.rows[0].lineNumber = 7
        workingDays = self.build_default_working_days_table()
        document = self.given_a_document_with_holidays(workingDays, holidays)

        exception = self.expect_conversion_exception(document)

        self.then_the_exception_is(exception, ColumnNumberException, 7)

    def test_holiday_row_with_wrong_formatted_date(self):
        holidays = self.build_holidays_table([
            ("02.01.2023 -- 06.01.2023 ", " Skiing ")])
        holidays.rows[0].lineNumber = 8
        workingDays = self.build_default_working_days_table()
        document = self.given_a_document_with_holidays(workingDays, holidays)

        exception = self.expect_conversion_exception(document)

        self.then_the_exception_is(exception, ValueConversionException, 8)
        self.assertEqual(exception.inputString, "02.01.2023 -- 06.01.2023")
    