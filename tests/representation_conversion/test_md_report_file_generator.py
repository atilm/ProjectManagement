import unittest
import datetime
from src.services.domain.report_generation.report_file_generator import ReportFileGenerator

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

| Id | Description | Estimate | Started | Completed | Workdays | Created    | Removed |
| -- | ----------- | -------- | ------- | --------- | -------- | ---------- | ------- |
| 1  | Task 1      | 1        |         |           |          | 04-12-2022 |         |
| 2  | Task 2      | 2        |         |           |          | 04-12-2022 |         |

# Completed Stories

| Id | Description | Estimate | Started | Completed  | Workdays | Created    | Removed |
| -- | ----------- | -------- | ------- | ---------- | -------- | ---------- | ------- |
| 4  | Task 4      | 5        |         | 01-03-2022 | 10.0     | 04-12-2022 |         |

# Removed Stories

| Id | Description | Estimate | Started | Completed | Workdays | Created | Removed |
| -- | ----------- | -------- | ------- | --------- | -------- | ------- | ------- |
"""

expectedReport = """# Planning Report

| Id | Description | Days | Completion date |
| -- | ----------- | ---- | --------------- |
| 1  | Task 1      | 2.0  | 22-12-2022      |
| 2  | Task 2      | 4.0  | 28-12-2022      |

"""

class ReportFileGeneratorTest(unittest.TestCase):
    def test_generate_report_from_planning_file_content(self):
        generator = ReportFileGenerator()

        startDate = datetime.date(2022,12,20)

        actualreport = generator.generate(planningFileContent, startDate)

        self.assertEqual(actualreport, expectedReport)