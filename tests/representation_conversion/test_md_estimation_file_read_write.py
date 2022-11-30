import unittest
from src.services.markdown.markdown_parser import *
from src.services.markdown.markdown_writer import *
from src.services.domain.representation_reading.md_estimation_file_to_model_converter import *
from src.services.domain.representation_writing.md_model_to_estimation_file_converter import *

class MarkdownEstimationFileTest(unittest.TestCase):
    
    def when_the_file_is_read_and_written_again(self, input: str) -> str:
        parser = MarkdownParser()
        document = parser.parse(input)
        
        converter = MarkdownEstimationFileToModelConverter()
        repo = converter.convert(document)

        backConverter = ModelToMarkdownEstimationDocumentConverter()
        outputDocument = backConverter.convert(repo)

        writer = MarkdownWriter()
        output = writer.write(outputDocument)

        return output


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
            "| --- | ---  |\n"\
            "| ID-1 | Desc 1 |\n"\
            "| ID-2 | Desc 2 |\n"\
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




