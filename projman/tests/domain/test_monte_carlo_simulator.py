from projman.src.domain.monte_carlo_simulator import *
from projman.src.domain.working_day_repository import WorkingDayRepository
from .domain_test_case import DomainTestCase
import datetime

class ExpectedValueSelector(RandomSelector):
    def select(self, interval: ConfidenceInterval) -> float:
        return interval.expected_value

class MonteCarloTestCase(DomainTestCase):
    def when_a_simulation_is_run(self, repo_collection: RepositoryCollection, start_date: datetime.date, num_simulations: int = 1, random_selector: RandomSelector = None) -> MonteCarloSimulationResult:
        if random_selector is None:
            random_selector = ExpectedValueSelector()
        simulator = MonteCarloSimulator(repo_collection, num_simulations, random_selector)
        return simulator.run_simulation(start_date)

class the_user_can_run_a_monte_carlo_simulation(MonteCarloTestCase):
    def test_run_simulation_returns_a_result(self):
        repo = self.given_an_empty_repository()
        repo_collection = RepositoryCollection(repo, self.given_a_working_days_repository_collection([WorkingDayRepository()]))

        result = self.when_a_simulation_is_run(repo_collection, datetime.date(2022, 1, 1))

        self.assertSetEqual(result.warnings, {'No velocity could be calculated.'})

        # then a simulation result is returned
        self.assertIsInstance(result, MonteCarloSimulationResult)

    def test_simulation_with_one_run(self):
        repo_collection = self.given_a_repository_collection([
            self.completed_task(datetime.date(2022, 1, 1), 3, 6),
            self.todo_task(5),
            self.todo_task(3)
        ], [WorkingDayRepository()])

        result = self.when_a_simulation_is_run(repo_collection, datetime.date(2022, 1, 1))

        self.assertListEqual(result.warnings, [])

        # then the sum of the durations is returned
        self.assertListEqual(result.bin_edges, [datetime.date(2022, 1, 17)])
        self.assertListEqual(result.frequencies, [1])

    def test_simulation_with_three_runs(self):
        repo_collection = self.given_a_repository_collection([
            self.completed_task(datetime.date(2022, 1, 1), 3, 6),
            self.todo_task(5),
            self.todo_task(3)
        ], [WorkingDayRepository()])

        number_of_runs = 3

        result = self.when_a_simulation_is_run(repo_collection, datetime.date(2022, 1, 1), number_of_runs)

        self.assertListEqual(result.warnings, [])

        # then the sum of the durations is returned
        self.assertListEqual(result.bin_edges, [datetime.date(2022, 1, 17)])
        self.assertListEqual(result.frequencies, [3])

    def test_simulation_with_real_random_selector(self):
        repo_collection = self.given_a_repository_collection([
            self.completed_task(datetime.date(2022, 1, 1), 3, 6),
            self.todo_task(5),
            self.todo_task(3)
        ], [WorkingDayRepository()])

        number_of_runs = 1000

        result = self.when_a_simulation_is_run(repo_collection, datetime.date(2022, 1, 1), number_of_runs, UniformRandomSelector())

        self.assertListEqual(result.warnings, [])

        # then the sum of the durations is returned
        self.assertGreaterEqual(len(result.bin_edges), 1)
        self.assertEqual(len(result.bin_edges), len(result.frequencies))
        self.assertEqual(sum(result.frequencies), number_of_runs)

    def test_percentiles_are_calculated(self):
        repo_collection = self.given_a_repository_collection([
            self.completed_task(datetime.date(2022, 1, 1), 3, 6),
            self.todo_task(5),
            self.todo_task(3)
        ], [WorkingDayRepository()])

        number_of_runs = 1000

        result = self.when_a_simulation_is_run(repo_collection, datetime.date(2022, 1, 1), number_of_runs, UniformRandomSelector())

        self.assertListEqual(result.warnings, [])

        # then the sum of the durations is returned
        self.assertGreaterEqual(result.percentiles[50], datetime.date(2022, 1, 15))
        self.assertGreaterEqual(result.percentiles[70], datetime.date(2022, 1, 17))
        self.assertGreaterEqual(result.percentiles[85], datetime.date(2022, 1, 17))
        self.assertGreaterEqual(result.percentiles[95], datetime.date(2022, 1, 17))