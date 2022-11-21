import unittest

from src.domain.tasks_repository import *
from src.services.markdown.markdown_document import *
from src.services.domain.representation_writing.md_model_to_planning_file_converter import *

class ConverterTestCase(unittest.TestCase):
    def given_a_repository(self) -> TaskRepository:
        return TaskRepository()

    def when_the_repo_is_converted(self, repo: TaskRepository) -> MarkdownDocument:
        converter = ModelToMarkdownPlanningDocumentConverter()
        return converter.convert(converter)

    def then_the_document_has_the_expected_structure(self, doc: MarkdownDocument):
        self.assertEqual(len(doc.getContent()), 7, doc)
        self._assertSection(0, "Planning", 0, doc)
        self._assertSection(1, "Stories To Do", 1, doc)
        self._assertTable(2, 8, 0, doc)
        self._assertSection(3, "Completed Stories", 1, doc)
        self._assertTable(4, 8, 0, doc)
        self._assertSection(5, "Removed Stories", 1, doc)
        self._assertTable(6, 8, 0, doc)

    def _assertSection(self, entryIndex : int, title: str, level: int, document : MarkdownDocument):
        entry = document.getContent()[entryIndex]
        self.assertIsInstance(entry, MarkdownSection)
        self.assertEqual(entry.title, title)
        self.assertEqual(entry.level, level)

    def _assertTable(self, entryIndex: int, colCount: int, rowCount: int, document: MarkdownDocument):
        entry = document.getContent()[entryIndex]
        self.assertIsInstance(entry, MarkdownTable)
        self.assertEqual(entry.getColumnCount(), colCount)
        self.assertEqual(entry.getRowCount(), rowCount)

class a_model_can_be_converted_into_a_planning_markdown_document(ConverterTestCase):
    def test_an_empty_repository_results_in_a_template_file(self):
        repo = self.given_a_repository()

        document = self.when_the_repo_is_converted(repo)

        self.then_the_document_has_the_expected_structure(document)