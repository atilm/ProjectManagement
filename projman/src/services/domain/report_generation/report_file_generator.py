from projman.src.services.markdown.markdown_writer import *
from projman.src.services.domain.report_generation.md_report_converter import *

class ReportFileGenerator:
    def __init__(self) -> None:
        self.reportConverter = ReportToMarkdownConverter()
        self.writer = MarkdownWriter()

    def generate(self, report: Report) -> str:
        reportDocument = self.reportConverter.convert(report)
        reportFileContent = self.writer.write(reportDocument)

        return reportFileContent
