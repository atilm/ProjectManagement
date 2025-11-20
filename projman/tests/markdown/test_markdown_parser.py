import unittest
from projman.src.services.markdown.markdown_parser import *

class ParserTestCase(unittest.TestCase):
    def when_the_input_is_parsed(self, input : str) -> MarkdownDocument:
        parser = MarkdownParser()
        return parser.parse(input)

    def the_parser_raises(self, exceptionType, input : str):
        parser = MarkdownParser()
        self.assertRaises(exceptionType, parser.parse, input)

    def then_the_document_entry_count_is(self, n : int, document : MarkdownDocument):
        self.assertEqual(len(document.getContent()), n)

    def then_entry_is_of_type(self, entryIndex : int, type, document : MarkdownDocument):
        self.assertIsInstance(self._getEntry(entryIndex, document), type)

    def then_entry_has_title(self, entryIndex : int, title : str, document : MarkdownDocument):
        entry = self._getEntry(entryIndex, document)
        self.assertEqual(entry.title, title)

    def then_the_entry_has_line_number(self, entryIndex : int, lineNumber : int, document : MarkdownDocument):
        entry = self._getEntry(entryIndex, document)
        self.assertEqual(entry.lineNumber, lineNumber)

    def then_the_entry_has_column_count(self, entryIndex : int, columnCount : int, document : MarkdownDocument):
        entry = self._getEntry(entryIndex, document)
        self.assertEqual(entry.getColumnCount(), columnCount)

    def then_the_entry_has_column_header(self, entryIndex : int, columnIndex : int, columnHeader : str, document : MarkdownDocument):
        entry = self._getEntry(entryIndex, document)
        self.assertEqual(entry.getColumnHeader(columnIndex), columnHeader)

    def then_the_entry_has_row_count(self, entryIdx : int, rowCount : int, document : MarkdownDocument):
        entry = self._getEntry(entryIdx, document)
        self.assertEqual(entry.getRowCount(), rowCount)

    def then_the_entry_has_table_entry(self, entryIdx : int, rowIdx : int, colIdx : int, content : str, document : MarkdownDocument):
        entry = self._getEntry(entryIdx, document)
        self.assertEqual(entry.rows[rowIdx].get(colIdx), content)

    def then_the_row_has_line_number(self, entryIdx : int, rowIdx : int, lineNumber : int, document : MarkdownDocument):
        entry = self._getEntry(entryIdx, document)
        self.assertEqual(entry.rows[rowIdx].lineNumber, lineNumber)

    def _getEntry(self, entryIndex : int, document : MarkdownDocument):
        return document.getContent()[entryIndex]

class the_parser_can_parse_sections(ParserTestCase):
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
        givenInput = ( "some line\n"
        "another line" )

        result = self.when_the_input_is_parsed(givenInput)

        self.then_the_document_entry_count_is(0, result)

    def test_the_section_title_is_parsed(self):
        givenInput = "# The only section"

        result = self.when_the_input_is_parsed(givenInput)

        self.then_entry_has_title(0, "The only section", result)

    def test_parsing_a_file_with_multiple_sections(self):
        givenInput = ( ""
        "\n"
        "## First Section \n"
        "\n"
        "#Second Section\n"
        "### Third Section\n"
        "\n" )

        result = self.when_the_input_is_parsed(givenInput)

        self.then_the_document_entry_count_is(3, result)
        self.then_entry_has_title(0, "First Section", result)
        self.then_the_entry_has_line_number(0, 2, result)
        self.then_entry_has_title(1, "Second Section", result)
        self.then_entry_has_title(2, "Third Section", result)
        self.then_the_entry_has_line_number(2, 5, result)

class the_parser_can_parse_tables(ParserTestCase):
    
    def test_parsing_a_table_with_only_a_header(self):
        givenInput = (""
        "| Header 1 | Header 2 |\n"
        "| - | - |")

        result = self.when_the_input_is_parsed(givenInput)

        self.then_the_document_entry_count_is(1, result)
        self.then_entry_is_of_type(0, MarkdownTable, result)

    def test_parsing_two_tables_with_only_headers(self):
        givenInput = (""
        "| Header 1 | Header 2 |\n"
        "| - | - |\n"
        "\n"
        "| Header 1 | Header 2 |\n"
        "| - | - |")

        result = self.when_the_input_is_parsed(givenInput)

        self.then_the_document_entry_count_is(2, result)
        self.then_entry_is_of_type(0, MarkdownTable, result)
        self.then_entry_is_of_type(1, MarkdownTable, result)

    def test_the_table_headers_are_parsed_correctly(self):
        givenInput = (""
        "| Header 1 |\n"
        "| - |\n"
        "\n"
        "| Id | Description |\n"
        "| - | - |")

        result = self.when_the_input_is_parsed(givenInput)

        self.then_the_entry_has_column_count(0, 1, result)
        self.then_the_entry_has_column_header(0, 0, "Header 1", result)
        self.then_the_entry_has_column_count(1, 2, result)
        self.then_the_entry_has_column_header(1, 0, "Id", result)
        self.then_the_entry_has_column_header(1, 1, "Description", result)

    def test_separator_line_must_be_preceded_by_matching_header(self):
        givenInput = (""
        "some other text\n"
        "| -- | -- |\n")

        self.the_parser_raises(TableRowException, givenInput)

    def test_table_rows_are_parsed(self):
        givenInput = (""
        "| Header 1 | Header 2 |\n"
        "| -------- | -------- |\n"
        "| 1.1 | 1.2 |\n"
        " | 2.1 | 2.2 |\n"
        "\n")

        result = self.when_the_input_is_parsed(givenInput)

        self.then_the_document_entry_count_is(1, result)
        self.then_the_entry_has_row_count(0, 2, result)
        self.then_the_row_has_line_number(0, 0, 3, result)
        self.then_the_row_has_line_number(0, 1, 4, result)
        self.then_the_entry_has_table_entry(0, 0, 0, "1.1", result)
        self.then_the_entry_has_table_entry(0, 0, 1, "1.2", result)
        self.then_the_entry_has_table_entry(0, 1, 0, "2.1", result)
        self.then_the_entry_has_table_entry(0, 1, 1, "2.2", result)