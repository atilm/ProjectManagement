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


