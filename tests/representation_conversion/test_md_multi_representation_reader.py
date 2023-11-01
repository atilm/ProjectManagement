import unittest
from typing import List
from src.services.domain.representation_reading.md_multi_representation_reader import MarkdownMultiRepresentationReader
from src.services.domain.representation_reading.md_planning_file_to_model_converter import MarkdownPlanningDocumentToModelConverter
import datetime

class ReadingWorkingDaysFromSeveralFiles(unittest.TestCase):
    def when_input_is_parsed(self, input_strings: List[str]):
        reader = MarkdownMultiRepresentationReader(MarkdownPlanningDocumentToModelConverter())
        return reader.read(input_strings)

    def given_a_planning_file(self):
        return """
# Planning

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

    def given_a_first_working_days_file(self):
        return """
# Tim's Holidays

# Working Days

| Mo | Tu | We | Th | Fr | Sa | Su |
| -- | -- | -- | -- | -- | -- | -- |
| x  | x  | x  | x  | x  |    |    |

# Holidays

| Dates                    | Description |
| ------------------------ | ----------- |
| 05-01-2023 -- 12-01-2023 | gone skiing |
"""

    def given_a_second_working_days_file(self):
        return """
# Tom's Holidays

# Working Days

| Mo | Tu | We | Th | Fr | Sa | Su |
| -- | -- | -- | -- | -- | -- | -- |
| x  | x  | x  | x  |    |    |    |

# Holidays

| Dates                    | Description |
| ------------------------ | ----------- |
| 08-02-2023 -- 10-02-2023 | hiking      |
"""

    def test_reading_several_empty_strings_returns_empty_repositories(self):
        repos = self.when_input_is_parsed(["", ""])

        self.assertEqual(len(repos.task_repository.tasks), 0)
        self.assertEqual(len(repos.working_days_repository_collection.repositories), 0)

    def test_information_from_several_files_is_merged_into_one_repository(self):
        tasks = self.given_a_planning_file()
        timsCalendar = self.given_a_first_working_days_file()
        tomsCalendar = self.given_a_second_working_days_file()

        repos = self.when_input_is_parsed([tasks, timsCalendar, tomsCalendar])

        self.assertEqual(len(repos.task_repository.tasks), 3)
        self.assertEqual(len(repos.working_days_repository_collection.repositories), 2)
        self.assertEqual(repos.working_days_repository_collection.get_working_day_capacity(datetime.date(2023, 2, 10)), 0.5, "because it's a friday")
        self.assertEqual(repos.working_days_repository_collection.get_working_day_capacity(datetime.date(2023, 1, 6)), 0.0, "because it's a friday during Tim's holidays")