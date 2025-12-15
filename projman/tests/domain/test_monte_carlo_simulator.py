from projman.src.domain.monte_carlo_simulator import *
from projman.src.domain.working_day_repository import WorkingDayRepository
from .domain_test_case import DomainTestCase
import datetime

class ExpectedValueSelector(RandomSelector):
    def select(self, interval: ConfidenceInterval) -> float:
        return interval.expected_value

class MonteCarloTestCase(DomainTestCase):
    def when_a_simulation_is_run(self, repo_collection: RepositoryCollection, start_date: datetime.date, num_simulations: int = 1) -> MonteCarloSimulationResult:
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

    def test_simulation(self):
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