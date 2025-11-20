from projman.tests.domain.domain_test_case import DomainTestCase
from projman.src.services.markdown.markdown_parser import *
from projman.src.services.markdown.markdown_writer import *
from projman.src.services.domain.representation_reading.md_estimation_file_to_model_converter import *
from projman.src.services.domain.representation_writing.md_model_to_estimation_file_converter import *
from projman.src.domain.working_day_repository_collection import *

class MarkdownEstimationFileTest(DomainTestCase):
    
    def when_the_file_is_read_and_written_again(self, input: str) -> str:
        repos = self._parse_to_repo(input)

        return self.when_an_estimation_file_is_generated(repos)

    def when_an_estimation_file_is_generated(self, repos: RepositoryCollection) -> str:
        converter = ModelToMarkdownEstimationDocumentConverter()
        outputDocument = converter.convert(repos)
        writer = MarkdownWriter()
        output = writer.write(outputDocument)

        return output

    def expect_parse_exception(self, input: str) -> str:
        try:
            self._parse_to_repo(input)
        except Exception as e:
            return e

        self.fail("Conversion did not raise an exception")

    def _parse_to_repo(self, input: str) -> RepositoryCollection:
        parser = MarkdownParser()
        document = parser.parse(input)

        converter = MarkdownEstimationFileToModelConverter()
        repoCollection = converter.convert(document)
        return repoCollection

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
            "| Id  | Project | Desc |\n"\
            "| - | - | -  |\n"\
            "| ID-1| Project X | Desc 1     |\n"\
            "| ID-2    | Project Y | Desc 2 |\n"\
            "\n"

        resultContent = self.when_the_file_is_read_and_written_again(givenAnEstimationFileContent)

        expectedContent = ""\
            "# Estimation\n"\
            "\n"\
            "## Unestimated\n"\
            "\n"\
            "| Id   | Project   | Desc   |\n"\
            "| ---- | --------- | ------ |\n"\
            "| ID-1 | Project X | Desc 1 |\n"\
            "| ID-2 | Project Y | Desc 2 |\n"\
            "\n"

        self.assertEqual(resultContent, expectedContent)

    def test_an_estimation_file_with_estimated_tasks_can_be_read_and_written(self):
        givenFileContent = ""\
            "# Estimation\n"\
            "\n"\
            "## 13\n"\
            "\n"\
            "| Id   | Project | Desc   |\n"\
            "| ---- | ------- | ------ |\n"\
            "| ID-1 | Proj 1  | Desc 1 |\n"\
            "\n"\
            "## 3\n"\
            "\n"\
            "| Id   | Project | Desc   |\n"\
            "| ---- | ------- | ------ |\n"\
            "| ID-2 | Proj 2  | Desc 2 |\n"\
            "| ID-3 | Proj 1  | Desc 3 |\n"\
            "\n"\
            "## Unestimated\n"\
            "\n"\
            "| Id   | Project | Desc   |\n"\
            "| ---- | ------- | ------ |\n"\
            "| ID-4 | Proj 2  | Desc 4 |\n"\
            "| ID-5 | Proj 1  | Desc 5 |\n"\
            "\n"

        resultContent = self.when_the_file_is_read_and_written_again(givenFileContent)

        self.assertEqual(resultContent, givenFileContent)

    def test_only_the_three_newest_tasks_of_each_estimation_level_are_used_as_reference_stories(self):
        tasks = [
            self.completed_task(datetime.date(2023, 1, 1), 1, 1, "Proj 1"),
            self.completed_task(datetime.date(2023, 1, 2), 1, 1, "Proj 2"),
            self.completed_task(datetime.date(2023, 1, 3), 1, 1, "Proj 3"),
            self.completed_task(datetime.date(2023, 1, 4), 1, 1, "Proj 4"),
        ]
        repo = self.given_a_repository_with_tasks(tasks)

        workingDaysRepoCollection = WorkingDayRepositoryCollection()
        workingDaysRepoCollection.add(WorkingDayRepository())
        resultContent = self.when_an_estimation_file_is_generated(RepositoryCollection(repo, workingDaysRepoCollection))

        expectedFilecontent = ""\
            "# Estimation\n"\
            "\n"\
            "## 1\n"\
            "\n"\
            "| Id | Project | Desc |\n"\
            "| -- | ------- | ---- |\n"\
            f"| {tasks[1].id}  | Proj 2  |      |\n"\
            f"| {tasks[2].id}  | Proj 3  |      |\n"\
            f"| {tasks[3].id}  | Proj 4  |      |\n"\
            "\n"\

        self.assertEqual(expectedFilecontent, resultContent)

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

    def test_a_wrong_number_of_table_columns_raises_an_exception(self):
        givenContent = ""\
            "# Estimation\n"\
            "\n"\
            "## 13\n"\
            "\n"\
            "| Id   | Project | Desc   |\n"\
            "| ---- | ------- | ------ |\n"\
            "| ID-1 | Proj 1  | Desc 1 |\n"\
            "| ID-2 |\n"

        error = self.expect_parse_exception(givenContent)

        self.then_the_exception_is(error, ColumnNumberException, 8)
            

