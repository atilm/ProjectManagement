import unittest
from src.services.markdown.markdown_parser import *
from src.services.markdown.markdown_writer import *
from src.services.domain.representation_reading.md_estimation_file_to_model_converter import *
from src.services.domain.representation_writing.md_model_to_estimation_file_converter import *

class MarkdownEstimationFileTest(unittest.TestCase):
    
    def when_the_file_is_read_and_written_again(self, input: str) -> str:
        repo = self._parse_to_repo(input)

        backConverter = ModelToMarkdownEstimationDocumentConverter()
        outputDocument = backConverter.convert(repo)

        writer = MarkdownWriter()
        output = writer.write(outputDocument)

        return output

    def expect_parse_exception(self, input: str) -> str:
        try:
            self._parse_to_repo(input)
        except Exception as e:
            return e

        self.fail("Conversion did not raise an exception")

    def _parse_to_repo(self, input: str) -> TaskRepository:
        parser = MarkdownParser()
        document = parser.parse(input)

        converter = MarkdownEstimationFileToModelConverter()
        repoCollection = converter.convert(document)
        return repoCollection.task_repository

    def then_the_exception_is(self, e : Exception, expectedType, lineNumber: int):
        self.assertIsInstance(e, expectedType)
        self.assertEqual(e.lineNumber, lineNumber)
        

    def test_an_empty_estimation_file_can_be_read_and_written(self):
        givenAnEmptyEstimationFileContent =  ""

        resultFileContent = self.when_the_file_is_read_and_written_again(givenAnEmptyEstimationFileContent)

        expectedContent = "# Estimation\n\n"

        self.assertEqual(resultFileContent, expectedContent)

    def test_an_estimation_file_containing_two_unestimated_tasks_can_be_read_and_written(self):
        givenAnEstimationFileContent = ""\
            "# Estimation\n"\
            "\n"\
            "## Unestimated\n"\
            "\n"\
            "| Id  | Desc |\n"\
            "| - | -  |\n"\
            "| ID-1| Desc 1     |\n"\
            "| ID-2    | Desc 2 |\n"\
            "\n"

        resultContent = self.when_the_file_is_read_and_written_again(givenAnEstimationFileContent)

        expectedContent = ""\
            "# Estimation\n"\
            "\n"\
            "## Unestimated\n"\
            "\n"\
            "| Id   | Desc   |\n"\
            "| ---- | ------ |\n"\
            "| ID-1 | Desc 1 |\n"\
            "| ID-2 | Desc 2 |\n"\
            "\n"

        self.assertEqual(resultContent, expectedContent)

    def test_an_estimation_file_with_estimated_tasks_can_be_read_and_written(self):
        givenFileContent = ""\
            "# Estimation\n"\
            "\n"\
            "## 13\n"\
            "\n"\
            "| Id   | Desc   |\n"\
            "| ---- | ------ |\n"\
            "| ID-1 | Desc 1 |\n"\
            "\n"\
            "## 3\n"\
            "\n"\
            "| Id   | Desc   |\n"\
            "| ---- | ------ |\n"\
            "| ID-2 | Desc 2 |\n"\
            "| ID-3 | Desc 3 |\n"\
            "\n"\
            "## Unestimated\n"\
            "\n"\
            "| Id   | Desc   |\n"\
            "| ---- | ------ |\n"\
            "| ID-4 | Desc 4 |\n"\
            "| ID-5 | Desc 5 |\n"\
            "\n"

        resultContent = self.when_the_file_is_read_and_written_again(givenFileContent)

        self.assertEqual(resultContent, givenFileContent)

    def test_an_unexpected_section_raises_an_exception(self):
        givenContent = ""\
            "# Estimation\n"\
            "\n"\
            "## 0,5\n" # no valid float format

        error = self.expect_parse_exception(givenContent)

        self.then_the_exception_is(error, UnexpectedSectionException, 3)

    def test_an_unexpected_table_header_raises_an_exception(self):
        givenContent = ""\
            "# Estimation\n"\
            "\n"\
            "## 13\n"\
            "\n"\
            "| Id   |\n"\
            "| ---- |\n"\
            "| ID-1 |\n"

        error = self.expect_parse_exception(givenContent)

        self.then_the_exception_is(error, HeaderFormatException, 5)

    def test_an_wrong_number_of_table_columns_raises_an_exception(self):
        givenContent = ""\
            "# Estimation\n"\
            "\n"\
            "## 13\n"\
            "\n"\
            "| Id   | Desc   |\n"\
            "| ---- | ------ |\n"\
            "| ID-1 | Desc 1 |\n"\
            "| ID-2 |\n"

        error = self.expect_parse_exception(givenContent)

        self.then_the_exception_is(error, ColumnNumberException, 8)
            

