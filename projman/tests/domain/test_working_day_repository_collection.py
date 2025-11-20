
from .domain_test_case import DomainTestCase
from projman.src.domain.working_day_repository_collection import *
from projman.src.domain.free_range import FreeRange
from projman.src.domain import weekdays

class calculate_capacity_from_zero_to_several_repositories(DomainTestCase):
    def test_an_empty_repository_collection_always_returns_zero(self):
        repos = WorkingDayRepositoryCollection()

        self.assertEqual(0.0, repos.get_working_day_capacity(datetime.date(2023, 10, 7)))

    def test_adding_one_repository(self):
        holidays = FreeRange(datetime.date(2023, 10, 9), datetime.date(2023, 10, 10), "")

        holidays_repo = self.given_a_working_days_repository(
            [weekdays.SATURDAY, weekdays.SUNDAY],
            [holidays])
        
        repo_collection = self.given_a_working_days_repository_collection([holidays_repo])
        
        self.then_the_given_day_has_the_capacity(holidays.lastFreeDay + datetime.timedelta(days=1), 1.0, repo_collection)

    def test_calculate_capacity_from_three_repositories(self):
        working_days_A = self.given_a_working_days_repository([], [FreeRange(datetime.date(2023, 10, 10), datetime.date(2023, 10, 10), "")])
        working_days_B = self.given_a_working_days_repository([], [FreeRange(datetime.date(2023, 10, 10), datetime.date(2023, 10, 11), "")])
        working_days_C = self.given_a_working_days_repository([], [FreeRange(datetime.date(2023, 10, 10), datetime.date(2023, 10, 12), "")])

        collection = self.given_a_working_days_repository_collection([working_days_A, working_days_B, working_days_C])
        
        self.then_the_given_day_has_the_capacity(datetime.date(2023, 10, 10), 0.0, collection)
        self.then_the_given_day_has_the_capacity(datetime.date(2023, 10, 11), 1.0/3.0, collection)
        self.then_the_given_day_has_the_capacity(datetime.date(2023, 10, 12), 2.0/3.0, collection)
        self.then_the_given_day_has_the_capacity(datetime.date(2023, 10, 13), 1.0, collection)

    def then_the_given_day_has_the_capacity(self, day: datetime.date, expected_capacity: float, repos: WorkingDayRepositoryCollection):
        self.assertAlmostEqual(expected_capacity, repos.get_working_day_capacity(day))

class the_collection_returns_the_set_of_all_free_ranges(DomainTestCase):
    def test_an_empty_repository_collection_returns_an_empty_set_of_free_ranges(self):
        empty_collection = self.given_a_working_days_repository_collection([])

        self.assertEqual(len(empty_collection.get_free_ranges()), 0)

    def test_a_collection_of_two_repositories_returns_all_free_ranges(self):
        working_days_A = self.given_a_working_days_repository([], [FreeRange(datetime.date(2023, 10, 10), datetime.date(2023, 10, 10), "range a")])
        working_days_B = self.given_a_working_days_repository([], [FreeRange(datetime.date(2023, 10, 10), datetime.date(2023, 10, 11), "range b")])

        collection = self.given_a_working_days_repository_collection([working_days_A, working_days_B])

        returned_ranges = collection.get_free_ranges()

        self.assertEqual(len(returned_ranges), 2)
        self.assertTrue(any(r.description == "range a" for r in returned_ranges))
        self.assertTrue(any(r.description == "range b" for r in returned_ranges))
