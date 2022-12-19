from src.services.markdown.markdown_parser import *
from src.services.markdown.markdown_writer import *
from src.services.domain.representation_reading.md_planning_file_to_model_converter import *
from src.services.domain.report_generation.md_report_converter import *
from src.domain.report_generator import ReportGenerator

class ReportFileGenerator:
    def __init__(self) -> None:
        self.parser = MarkdownParser()
        self.planningFileConverter = MarkdownPlanningDocumentToModelConverter()
        self.reportGenerator = ReportGenerator()
        self.reportConverter = ReportToMarkdownConverter()
        self.writer = MarkdownWriter()

    def generate(self, planningFileContent: str, startDate: datetime.date) -> str:
        planningDocument = self.parser.parse(planningFileContent)
        repos = self.planningFileConverter.convert(planningDocument)

        report = self.reportGenerator.generate(repos, startDate)
        
        reportDocument = self.reportConverter.convert(report)
        reportFileContent = self.writer.write(reportDocument)

        return reportFileContent
