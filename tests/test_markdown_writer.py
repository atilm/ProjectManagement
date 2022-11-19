import unittest
from src.services.markdown_writer import *
from src.services.markdown_document_builder import *

class MarkdownWriterTest(unittest.TestCase):
    def when_the_document_is_written(self, document : MarkdownDocument) -> str:
        writer = MarkdownWriter()
        return writer.write(document)

    def test_writing_an_empty_document(self):
        givenAnEmptyDocument = MarkdownDocumentBuilder().build()

        output = self.when_the_document_is_written(givenAnEmptyDocument)

        self.assertEqual(output, "")

    @unittest.skip
    def test_writing_a_whole_document(self):
        givenADocument = MarkdownDocumentBuilder()\
        .withSection("Section 1", 0)\
        .withSection("Section 2", 2)\
        .withTable(MarkdownTableBuilder()\
            .withHeader("Id", "Task")\
            .withRow("1", "Wash dishes")\
            .withHeader("2", "Grocery shopping")\
            .build())\
        .withSection("Section 3", 1)\
        .build()

        output = self.when_the_document_is_written(givenADocument)

        expectedOutput = (""
        "# Section 1\n"
        "\n"
        "### Section 2\n"
        "\n"
        "| Id | Task             |\n"
        "| -- | ---------------- |\n"
        "| 1  | Wash dishes      |\n"
        "| 2  | Grocery shopping |\n"
        "\n"
        "## Section 3\n"
        "\n")

        self.assertEqual(output, expectedOutput)