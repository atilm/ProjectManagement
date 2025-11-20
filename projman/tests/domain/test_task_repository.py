from .domain_test_case import DomainTestCase
from projman.src.domain.tasks_repository import *

class adding_and_retrieving_tasks(DomainTestCase):
    def expect_exception(self, action) -> Exception:
        try:
            action()
            self.fail("Expected an exception")
        except Exception as e:
            return e

    def test_exception_on_get_nonexisting_id(self):
        repo = self.given_an_empty_repository()

        self.assertRaises(TaskIdNotFoundException, lambda: self.when_the_user_retrieves_a_task_id("1", repo))

    def test_add_and_retrieve_one_task(self):
        task = Task("1", "", "")
        
        repo = self.given_a_repository_with_tasks([task])

        self.then_the_repo_returns_the_task(task.id, repo)

    def test_cannot_add_two_tasks_with_same_id(self):
        task1 = Task("id7", "", "")
        task2 = Task("id7", "", "")

        repo = self.given_a_repository_with_tasks([task1])
        
        action = lambda: self.when_a_task_is_added(task2, repo)
        error = self.expect_exception(action)
        self.assertIsInstance(error, TaskIdConflictException)
        self.assertEqual(error.taskId, "id7")

class updating_estimates(DomainTestCase):
    def test_several_estimates_can_be_updated(self):
        task1 = Task("1", "", "")
        task2 = Task("2", "", "")
        task3 = Task("3", "", "")

        estimatedTask1 = Task("1", "", "")
        estimatedTask1.estimate = 1
        estimatedTask2 = Task("2", "", "")
        estimatedTask2.estimate = 3

        repo = self.given_a_repository_with_tasks([task1, task2, task3])

        # when the repo is updated
        repo.updateEstimates([estimatedTask1, estimatedTask2])

        self.then_the_repo_contains_estimated_task("1", 1, repo)
        self.then_the_repo_contains_estimated_task("2", 3, repo)
        self.then_the_repo_contains_estimated_task("3", None, repo)
