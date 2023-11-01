import unittest
from datetime import date

from src.domain.tasks_repository import *
from src.domain.working_day_repository_collection import *
from src.domain import weekdays
from src.services.markdown.markdown_document import *
from src.services.domain.representation_writing.md_model_to_planning_file_converter import *

workingDaysTableIndex = 2
holidaysTableIndex = 4
todoTableIndex = 6
completedTableIndex = 8
removedTableIndex = 10

task_table_col_count = 8
default_project_name = "Project X"


class ConverterTestCase(unittest.TestCase):
    def given_a_task_repository(self) -> TaskRepository:
        return TaskRepository()

    def given_a_days_repository(self) -> WorkingDayRepository:
        return WorkingDayRepository()

    def add_todo_task(self, repo: TaskRepository, id: str, description: str):
        task = Task(id, description, default_project_name)
        task.estimate = 3
        task.createdDate = date(2022, 3, 1)
        repo.add(task)

    def add_completed_task(self, repo: TaskRepository, id: str, description: str):
        task = Task(id, description, default_project_name)
        task.estimate = 4
        task.startedDate = date(2022, 3, 2)
        task.completedDate = date(2022, 3, 4)
        task.createdDate = date(2022, 3, 1)
        repo.add(task)

    def add_removed_task(self, repo: TaskRepository, id: str, description: str):
        task = Task(id, description, default_project_name)
        task.estimate = 5
        task.startedDate = date(2022, 3, 2)
        task.createdDate = date(2022, 3, 1)
        task.removedDate = date(2022, 3, 3)
        repo.add(task)

    def when_the_repo_is_converted(self, taskRepo: TaskRepository) -> MarkdownDocument:
        converter = ModelToMarkdownPlanningDocumentConverter()
        workingDaysRepoCollection = WorkingDayRepositoryCollection()
        workingDaysRepoCollection.add(WorkingDayRepository())
        repos = RepositoryCollection(taskRepo, workingDaysRepoCollection)
        return converter.convert(repos)

    def when_the_repos_are_converted(self, taskRepo: TaskRepository, daysRepo: WorkingDayRepository) -> MarkdownDocument:
        converter = ModelToMarkdownPlanningDocumentConverter()
        workingDaysRepoCollection = WorkingDayRepositoryCollection()
        workingDaysRepoCollection.add(daysRepo)
        return converter.convert(RepositoryCollection(taskRepo, workingDaysRepoCollection))

    def then_the_document_has_the_expected_structure(self, doc: MarkdownDocument):
        self.assertEqual(len(doc.getContent()), 11, doc)
        self._assertSection(0, "Planning", 0, doc)
        self._assertSection(1, "Working Days", 1, doc)
        self._assertTableColumns(workingDaysTableIndex, 7, doc)
        self._assertSection(3, "Holidays", 1, doc)
        self._assertTableColumns(holidaysTableIndex, 2, doc)
        self._assertSection(5, "Stories To Do", 1, doc)
        self._assertTableColumns(todoTableIndex, task_table_col_count, doc)
        self._assertSection(7, "Completed Stories", 1, doc)
        self._assertTableColumns(completedTableIndex, task_table_col_count, doc)
        self._assertSection(9, "Removed Stories", 1, doc)
        self._assertTableColumns(removedTableIndex, task_table_col_count, doc)

    def _assertSection(self, entryIndex : int, title: str, level: int, document : MarkdownDocument):
        entry = document.getContent()[entryIndex]
        self.assertIsInstance(entry, MarkdownSection)
        self.assertEqual(entry.title, title)
        self.assertEqual(entry.level, level)

    def _assertTableColumns(self, entryIndex: int, colCount: int, document: MarkdownDocument):
        entry = document.getContent()[entryIndex]
        self.assertIsInstance(entry, MarkdownTable)
        self.assertEqual(entry.getColumnCount(), colCount)

    def _assertTable(self, entryIndex: int, colCount: int, rowCount: int, document: MarkdownDocument) -> MarkdownTable:
        entry = document.getContent()[entryIndex]
        self.assertIsInstance(entry, MarkdownTable)
        self.assertEqual(entry.getColumnCount(), colCount)
        self.assertEqual(entry.getRowCount(), rowCount)
        return entry

    def _assertRow(self, table: MarkdownTable, rowIndex: int, expectedCells: list) -> None:
        self.assertEqual(table.rows[rowIndex]._cells, expectedCells)

class a_model_can_be_converted_into_a_planning_markdown_document(ConverterTestCase):
    def test_an_empty_repository_results_in_a_template_file(self):
        repo = self.given_a_task_repository()

        document = self.when_the_repo_is_converted(repo)

        self.then_the_document_has_the_expected_structure(document)

    def test_a_repository_with_two_todo_tasks(self):
        repo = self.given_a_task_repository()
        self.add_todo_task(repo, "1", "Todo task 1")
        self.add_todo_task(repo, "2", "Todo task 2")

        document = self.when_the_repo_is_converted(repo)

        table = self._assertTable(todoTableIndex, task_table_col_count, 2, document)
        self.assertEqual(table.rows[0]._cells, ["1", default_project_name, "Todo task 1", "3", "", "", "01-03-2022", ""])
        self.assertEqual(table.rows[1]._cells, ["2", default_project_name, "Todo task 2", "3", "", "", "01-03-2022", ""])

    def test_a_repository_with_all_task_kinds(self):
        repo = self.given_a_task_repository()
        self.add_todo_task(repo, "1", "Todo task")
        self.add_completed_task(repo, "2", "Completed task")
        self.add_removed_task(repo, "3", "Removed task")

        document = self.when_the_repo_is_converted(repo)

        todoTable = self._assertTable(todoTableIndex, task_table_col_count, 1, document)
        completedTable = self._assertTable(completedTableIndex, task_table_col_count, 1, document)
        removedTable = self._assertTable(removedTableIndex, task_table_col_count, 1, document)

        self.assertEqual(todoTable.rows[0]._cells, ["1", default_project_name, "Todo task", "3", "", "", "01-03-2022", ""])
        self.assertEqual(completedTable.rows[0]._cells, ["2", default_project_name, "Completed task", "4", "02-03-2022", "04-03-2022", "01-03-2022", ""])
        self.assertEqual(removedTable.rows[0]._cells, ["3", default_project_name, "Removed task", "5", "02-03-2022", "", "01-03-2022", "03-03-2022"])


    def test_a_repository_with_all_working_days(self):
        taskRepo = self.given_a_task_repository()
        daysRepo = WorkingDayRepository()

        document = self.when_the_repos_are_converted(taskRepo, daysRepo)

        workingDaysTable = self._assertTable(workingDaysTableIndex, 7, 1, document)
        self._assertRow(workingDaysTable, 0, ["x"] * 7)

    def test_a_repository_with_some_free_weekdays(self):
        taskRepo = self.given_a_task_repository()
        daysRepo = WorkingDayRepository()
        daysRepo.set_free_weekdays(weekdays.MONDAY, weekdays.WEDNESDAY, weekdays.FRIDAY, weekdays.SUNDAY)

        document = self.when_the_repos_are_converted(taskRepo, daysRepo)

        workingDaysTable = self._assertTable(workingDaysTableIndex, 7, 1, document)
        self._assertRow(workingDaysTable, 0, ["", "x", "", "x", "", "x", ""])

    def test_a_repository_with_holidays(self):
        taskRepo = self.given_a_task_repository()
        daysRepo = self.given_a_days_repository()
        daysRepo.add_free_range(date(2022, 12, 21), date(2022, 12, 31), "Christmas holidays")
        daysRepo.add_free_range(date(2023, 1, 6), date(2023, 1, 6), "Holy Three Kings")

        document = self.when_the_repos_are_converted(taskRepo, daysRepo)

        holidaysTable = self._assertTable(holidaysTableIndex, 2, 2, document)
        self._assertRow(holidaysTable, 0, ["21-12-2022 -- 31-12-2022", "Christmas holidays"])
        self._assertRow(holidaysTable, 1, ["06-01-2023", "Holy Three Kings"])