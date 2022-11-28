import unittest
from datetime import date
from src.services.domain.representation_reading.md_planning_file_to_model_converter import *
from src.services.markdown.markdown_document_builder import *
from src.domain.task import Task
from tests.domain.domain_utilities.task_utilities import *

correctTableHeader = ["Id", "Description", "Estimate", "Started", "Completed", "Workdays", "Created", "Removed"]

class MarkdownPlanningDocumentToModelConverterTestCase(unittest.TestCase):
    def given_a_document_with_tables(self, todo: MarkdownTable, completed: MarkdownTable, removed: MarkdownTable) -> MarkdownDocument:
        return MarkdownDocumentBuilder()\
            .withSection("Planning", 0)\
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

    def when_the_document_is_converted(self, document: MarkdownDocument) -> TaskRepository:
        converter = MarkdownPlanningDocumentToModelConverter()
        return converter.convert(document)

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
