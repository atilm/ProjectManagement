import unittest
from .test_doubles.mock_file_reader import MockFileReader
from src.services.markdown_parser import *


class the_parser_can_parse_sections(unittest.TestCase):
    def when_the_input_is_parsed(self, input : str) -> MarkdownDocument:
        parser = MarkdownParser()
        return parser.parse(input)

    def then_the_document_entry_count_is(self, n : int, document : MarkdownDocument):
        self.assertEqual(len(document.getContent()), n)

    def then_entry_is_of_type(self, entryIndex : int, type, document : MarkdownDocument):
        self.assertIsInstance(document.getContent()[entryIndex], type)

    def then_entry_has_title(self, entryIndex : int, title : str, document : MarkdownDocument):
        self.assertEqual(document.getContent()[entryIndex].title, title)

    def test_parsing_an_empty_file(self):
        givenInput = ""

        result = self.when_the_input_is_parsed(givenInput)

        self.then_the_document_entry_count_is(0, result)

    def test_parsing_a_file_with_one_section(self):
        givenInput = "# The only section"

        result = self.when_the_input_is_parsed(givenInput)

        self.then_the_document_entry_count_is(1, result)
        self.then_entry_is_of_type(0, MarkdownSection, result)

    def test_parsing_a_file_with_unstructured_text(self):
        givenInput = "some line\nanother line"

        result = self.when_the_input_is_parsed(givenInput)

        self.then_the_document_entry_count_is(0, result)

    def test_the_section_title_is_parsed(self):
        givenInput = "# The only section"

        result = self.when_the_input_is_parsed(givenInput)

        self.then_entry_has_title(0, "The only section", result)

    def test_parsing_a_file_with_multiple_sections(self):
        givenInput = "\n## First Section \n\n#Second Section\n### Third Section\n\n"

        result = self.when_the_input_is_parsed(givenInput)

        self.then_the_document_entry_count_is(3, result)
        self.then_entry_has_title(0, "First Section", result)
        self.then_entry_has_title(1, "Second Section", result)
        self.then_entry_has_title(2, "Third Section", result)


