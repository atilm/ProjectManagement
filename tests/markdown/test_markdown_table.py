import unittest
from src.services.markdown.markdown_document import *
from src.services.markdown.markdown_document_builder import *

class the_table_reports_column_widths(unittest.TestCase):
    def then_the_table_has_column_widths(self, table : MarkdownTable, columnWidths : list):
        actualWidths = table.getColumnWidths()
        self.assertEqual(len(actualWidths), len(columnWidths))
        for actual, expected in zip(actualWidths, columnWidths):
            self.assertEqual(actual, expected)

    def test_a_table_without_rows_reports_the_header_widths(self):
        table = MarkdownTableBuilder()\
            .withHeader("Id", "", "Description")\
            .build()
        
        self.then_the_table_has_column_widths(table, [2, 0, 11])

    def test_a_table_with_two_headers(self):
        givenTable = MarkdownTableBuilder()\
            .withHeader("First", "Second")\
            .build()

        self.then_the_table_has_column_widths(givenTable, [5, 6])

    def test_a_table_with_two_rows(self):
        givenTable = MarkdownTableBuilder()\
            .withHeader("Id", "Description")\
            .withRow("ANT-1", "A long description")\
            .withRow("ANT-12", "short")\
            .build()

        self.then_the_table_has_column_widths(givenTable, [len("ANT-12"), len("A long description")])

    def test_a_table_with_variing_row_lengths(self):
        givenTable = MarkdownTableBuilder()\
            .withHeader("Id", "Description")\
            .withRow("ANT-1")\
            .withRow("ANT-12", "short", "third")\
            .build()

        self.then_the_table_has_column_widths(givenTable, [len("ANT-12"), len("Description"), len("third")])