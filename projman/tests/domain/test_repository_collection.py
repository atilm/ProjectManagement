from .domain_test_case import DomainTestCase
from projman.src.domain.repository_collection import mergeRepos
from projman.src.domain.free_range import FreeRange
from projman.src.services.utilities.date_utilities import dateRange
import datetime

class merging_repository_collections(DomainTestCase):
    def test_merging_two_empty_collections(self):
        first_collection = self.given_a_repository_collection([], [])
        second_collection = self.given_a_repository_collection([], [])

        merged_collection = mergeRepos(first_collection, second_collection)

        self.assertEqual(len(merged_collection.task_repository.tasks), 0)
        self.assertEqual(len(merged_collection.working_days_repository_collection.repositories), 0)

    def test_merging_non_conflicting_task_repos(self):
        first_task = self.todo_task(3, "proj1")
        first_collection = self.given_a_repository_collection([first_task], [])
        second_task = self.todo_task(5, "proj2")
        second_collection = self.given_a_repository_collection([second_task], [])

        merged_collection = mergeRepos(first_collection, second_collection)
        tasksRepo = merged_collection.task_repository

        self.assertEqual(len(tasksRepo.tasks), 2)
        self.then_the_repo_returns_the_task(first_task.id, tasksRepo)
        self.then_the_repo_returns_the_task(second_task.id, tasksRepo)

    def test_merging_working_day_repository_collections(self):
        first_repo = self.given_a_working_days_repository([], [FreeRange(datetime.date(2023,10, 1), datetime.date(2023, 10, 2), "")])
        second_repo = self.given_a_working_days_repository([], [FreeRange(datetime.date(2023, 10, 3), datetime.date(2023, 10, 4), "")])

        third_repo = self.given_a_working_days_repository([], [FreeRange(datetime.date(2023, 10, 5), datetime.date(2023, 10, 6), "")])
        fourth_repo = self.given_a_working_days_repository([], [FreeRange(datetime.date(2023, 10, 7), datetime.date(2023, 10, 8), "")])

        first_collection = self.given_a_repository_collection([], [first_repo, second_repo])
        second_collection = self.given_a_repository_collection([], [third_repo, fourth_repo])

        merged_collection = mergeRepos(first_collection, second_collection)

        self.assertEqual(len(merged_collection.working_days_repository_collection.repositories), 4)
        
        for currentDate in dateRange(datetime.date(2023,10, 1), datetime.date(2023, 10, 8)):
            self.assertEqual(merged_collection.working_days_repository_collection.get_working_day_capacity(currentDate), 3./4., "because there is always one worker on holidays")
