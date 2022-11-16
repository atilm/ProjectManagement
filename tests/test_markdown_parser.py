import unittest
from .test_doubles.mock_file_reader import MockFileReader
from src.services.markdown_parser import *

def given_a_parser() -> MarkdownParser:
    return MarkdownParser(MockFileReader())

def given_a_parser_and_a_file_content(fileContent : str) -> MarkdownParser:
    mockFileReader = MockFileReader()
    mockFileReader.setup(fileContent)
    return MarkdownParser(mockFileReader)

class the_parser_can_parse_sections(unittest.TestCase):
    def test_parsing_an_empty_file(self):
        parser = given_a_parser()

        result = parser.parse("fileName.md")

        self.assertEqual(result.getContent(), [])

    def test_parsing_a_file_with_one_section(self):
        parser = given_a_parser_and_a_file_content("# The only section")

        result = parser.parse("fileName.md")

        self.assertEqual(len(result.getContent()), 1)
        self.assertIsInstance(result.getContent()[0], Section)

    def test_parsing_a_file_with_unstructured_text(self):
        parser = given_a_parser_and_a_file_content(
            "some line\n"
            "another line"
        )

        result = parser.parse("fileName.md")

        self.assertEqual(len(result.getContent()), 0)

    def test_the_section_title_is_parsed(self):
        parser = given_a_parser_and_a_file_content("# The only section")

        result = parser.parse("fileName.md")

        section = result.getContent()[0]

        self.assertEqual(section.title, "The only section")

    def test_parsing_a_file_with_multiple_sections(self):
        parser = given_a_parser_and_a_file_content(
            "\n"
            "## First Section \n"
            "\n"
            "#Second Section\n"
            "### Third Section\n"
            "\n")

        result = parser.parse("fileName.md")

        self.assertEqual(len(result.getContent()), 3)
        self.assertEqual(result.getContent()[0].title, "First Section")
        self.assertEqual(result.getContent()[1].title, "Second Section")
        self.assertEqual(result.getContent()[2].title, "Third Section")


