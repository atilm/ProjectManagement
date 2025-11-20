import unittest
import datetime
from projman.src.services.domain.report_generation.report_file_generator import ReportFileGenerator
from projman.src.services.markdown.markdown_parser import MarkdownParser
from projman.src.services.domain.representation_reading.md_planning_file_to_model_converter import MarkdownPlanningDocumentToModelConverter
from projman.src.domain.report_generator import *

planningFileContent = """
# Planning

# Working Days

| Mo | Tu | We | Th | Fr | Sa | Su |
| -- | -- | -- | -- | -- | -- | -- |
| x  | x  | x  | x  | x  |    |    |

# Holidays

| Dates                    | Description |
| ------------------------ | ----------- |
| 09-01-2023 -- 12-01-2023 | gone skiing |

# Stories To Do

| Id | Project | Description | Estimate | Started | Completed | Created    | Removed |
| -- | ------- | ----------- | -------- | ------- | --------- | ---------- | ------- |
| 1  | Proj 1  | Task 1      | 1        |         |           | 04-12-2022 |         |
| 2  | Proj 2  | Task 2      | 2        |         |           | 04-12-2022 |         |

# Completed Stories

| Id | Project | Description | Estimate | Started    | Completed  | Created    | Removed |
| -- | ------- | ----------- | -------- | ---------- | ---------- | ---------- | ------- |
| 4  | Proj  1 | Task 4      | 5        | 15-02-2022 | 28-02-2022 | 04-12-2022 |         |

# Removed Stories

| Id | Project | Description | Estimate | Started | Completed | Created | Removed |
| -- | ------- | ----------- | -------- | ------- | --------- | ------- | ------- |
"""

expectedReport = """# Planning Report

| Id | Project | Description | Days | Completion date                      |
| -- | ------- | ----------- | ---- | ------------------------------------ |
| 1  | Proj 1  | Task 1      | 2.0  | (20-12-2022, 22-12-2022, 24-12-2022) |
| 2  | Proj 2  | Task 2      | 4.0  | (23-12-2022, 28-12-2022, 30-12-2022) |

"""

class ReportFileGeneratorTest(unittest.TestCase):
    def given_a_report(self, planningFileContent: str) -> Report:
        parser = MarkdownParser()
        planningFileConverter = MarkdownPlanningDocumentToModelConverter()
        reportGenerator = ReportGenerator()

        startDate = datetime.date(2022,12,20)
        planningDocument = parser.parse(planningFileContent)
        repos = planningFileConverter.convert(planningDocument)
        return reportGenerator.generate(repos, startDate)

    def test_generate_report_from_planning_file_content(self):
        report = self.given_a_report(planningFileContent)

        generator = ReportFileGenerator()
        actualreport = generator.generate(report)

        self.assertEqual(actualreport, expectedReport)