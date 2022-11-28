import unittest
from datetime import date, datetime

from src.domain.tasks_repository import *
from src.services.markdown.markdown_document import *
from src.services.domain.representation_writing.md_model_to_planning_file_converter import *

class ConverterTestCase(unittest.TestCase):
    def given_a_repository(self) -> TaskRepository:
        return TaskRepository()

    def add_todo_task(self, repo: TaskRepository, id: str, description: str):
        task = Task(id, description)
        task.estimate = 3
        task.createdDate = date(2022, 3, 1)
        repo.add(task)

    def when_the_repo_is_converted(self, repo: TaskRepository) -> MarkdownDocument:
        converter = ModelToMarkdownPlanningDocumentConverter()
        return converter.convert(repo)

    def then_the_document_has_the_expected_structure(self, doc: MarkdownDocument):
        self.assertEqual(len(doc.getContent()), 7, doc)
        self._assertSection(0, "Planning", 0, doc)
        self._assertSection(1, "Stories To Do", 1, doc)
        self._assertTableColumns(2, 8, doc)
        self._assertSection(3, "Completed Stories", 1, doc)
        self._assertTableColumns(4, 8, doc)
        self._assertSection(5, "Removed Stories", 1, doc)
        self._assertTableColumns(6, 8, doc)

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

class a_model_can_be_converted_into_a_planning_markdown_document(ConverterTestCase):
    def test_an_empty_repository_results_in_a_template_file(self):
        repo = self.given_a_repository()

        document = self.when_the_repo_is_converted(repo)

        self.then_the_document_has_the_expected_structure(document)

    def test_a_repository_with_two_todo_tasks(self):
        repo = self.given_a_repository()
        self.add_todo_task(repo, "1", "Todo task 1")
        self.add_todo_task(repo, "2", "Todo task 2")

        document = self.when_the_repo_is_converted(repo)

        table = self._assertTable(2, 8, 2, document)
        self.assertEqual(table.rows[0]._cells, ["1", "Todo task 1", "3", "", "", "", "01-03-2022", ""])
        self.assertEqual(table.rows[1]._cells, ["2", "Todo task 2", "3", "", "", "", "01-03-2022", ""])


        
