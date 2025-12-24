from projman.tests.domain.domain_test_case import DomainTestCase
from projman.src.services.markdown.markdown_parser import *
from projman.src.services.markdown.markdown_writer import *
from projman.src.services.domain.representation_writing.md_model_to_calendar_file_converter import *
from projman.src.domain.working_day_repository_collection import *
from projman.src.domain import weekdays

class CalendarFileTest(DomainTestCase):
    maxDiff = None

    def when_calendar_files_are_generated(self, repos: RepositoryCollection) -> list[tuple[str, str]]:
        converter = ModelToCalendarFilesConverter()
        output = converter.convert(repos)

        writer = MarkdownWriter()
        result = [ (calendarFile.filename, writer.write(calendarFile.document)) for calendarFile in output ]

        return result

    def test_empty_repository_collection_results_in_no_calendar_files(self):
        repos = RepositoryCollection(self.given_an_empty_repository(), self.given_a_working_days_repository_collection([]))

        files = self.when_calendar_files_are_generated(repos)

        self.assertEqual(len(files), 0)

    def test_one_working_days_repository_with_default_name_and_without_free_days(self):
        task_repository = self.given_an_empty_repository()
        working_days_repositories = self.given_a_working_days_repository_collection([
            self.given_a_working_days_repository([], [])
        ])
        repos = RepositoryCollection(task_repository, working_days_repositories)

        files = self.when_calendar_files_are_generated(repos)

        self.assertEqual(len(files), 1)
        file = files[0]
        self.assertEqual(file[0], "Developer Name.md")

        expected_content = """# Calendar for Developer Name

## Working Days

| Mo | Tu | We | Th | Fr | Sa | Su |
| -- | -- | -- | -- | -- | -- | -- |
| x  | x  | x  | x  | x  | x  | x  |

## Holidays

| Dates | Description |
| ----- | ----------- |
|       |             |

"""
        self.assertEqual(file[1], expected_content)


    def test_calendar_files_can_be_written_from_a_repository_collection(self):
        task_repository = self.given_an_empty_repository()
        working_days_repositories = self.given_a_working_days_repository_collection([
            self.given_a_working_days_repository(
                [weekdays.WEDNESDAY, weekdays.SATURDAY, weekdays.SUNDAY],
                [FreeRange(datetime.date(2023, 10, 17), datetime.date(2023, 10, 17), "First Holiday"),
                 FreeRange(datetime.date(2023, 12, 24), datetime.date(2023, 12, 26), "Second Holiday")], "Alice"),
            self.given_a_working_days_repository([weekdays.SATURDAY, weekdays.SUNDAY], [FreeRange(datetime.date(2023, 10, 17), datetime.date(2023, 10, 17), "holiday")], "Bob")
        ])
        repos = RepositoryCollection(task_repository, working_days_repositories)

        files = self.when_calendar_files_are_generated(repos)

        self.assertEqual(len(files), 2)
        alice_file = files[0]
        self.assertEqual(alice_file[0], "Alice.md")

        expected_alice_content = """# Calendar for Alice

## Working Days

| Mo | Tu | We | Th | Fr | Sa | Su |
| -- | -- | -- | -- | -- | -- | -- |
| x  | x  |    | x  | x  |    |    |

## Holidays

| Dates                    | Description    |
| ------------------------ | -------------- |
| 17-10-2023               | First Holiday  |
| 24-12-2023 -- 26-12-2023 | Second Holiday |

"""

        self.assertEqual(alice_file[1], expected_alice_content)

        bob_file = files[1]
        self.assertEqual(bob_file[0], "Bob.md")

        expected_bob_content = """# Calendar for Bob

## Working Days

| Mo | Tu | We | Th | Fr | Sa | Su |
| -- | -- | -- | -- | -- | -- | -- |
| x  | x  | x  | x  | x  |    |    |

## Holidays

| Dates      | Description |
| ---------- | ----------- |
| 17-10-2023 | holiday     |

"""
        self.assertEqual(bob_file[1], expected_bob_content)

