from tests.domain.domain_test_case import DomainTestCase
from src.services.domain.representation_reading.md_tracking_file_to_model_converter import MarkdownTrackingFileToModelConverter
from src.services.domain.representation_writing.md_model_to_tracking_file_converter import ModelToMarkdownTrackingFileConverter
from src.domain.completion_date_history import CompletionDateHistory
from src.services.markdown.markdown_writer import MarkdownWriter
from src.services.markdown.markdown_parser import MarkdownParser

class MarkdownTrackingFileTest(DomainTestCase):
    def when_a_history_is_written(self, history: CompletionDateHistory) -> str:
        converter = ModelToMarkdownTrackingFileConverter()
        outputDocument = converter.convert(history)
        writer = MarkdownWriter()
        return writer.write(outputDocument)
    
    def when_a_file_is_read(self, file_content: str) -> CompletionDateHistory:
        converter = MarkdownTrackingFileToModelConverter()
        parser = MarkdownParser()
        markdown_document = parser.parse(file_content)
        history = converter.convert(markdown_document)
        return history
        
    
    def test_write_an_empty_history(self):
        project_id = "project 1"
        empty_history = CompletionDateHistory(project_id)

        file_content = self.when_a_history_is_written(empty_history)

        expected_content = """# project 1 completion dates

| Date | Earliest | Probable | Latest | Comment |
| ---- | -------- | -------- | ------ | ------- |

"""

        self.assertEqual(file_content, expected_content)

    def test_read_and_write_a_history(self):
        file_input = """# project 2 completion dates

| Date       | Earliest   | Probable   | Latest     | Comment                      |
| ---------- | ---------- | ---------- | ---------- | ---------------------------- |
| 28-10-2023 | 01-11-2023 | 02-11-2023 | 03-11-2023 |                              |
| 29-10-2023 | 04-11-2023 | 05-11-2023 | 06-11-2023 | delayed by fix for project 1 |

"""

        history = self.when_a_file_is_read(file_input)
        file_output = self.when_a_history_is_written(history)
        self.assertEqual(file_output, file_input)