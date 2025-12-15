from projman.src.domain import task
from projman.src.domain.fibonacci_sequence import FibonacciSequence
import projman.src.domain.project_calculation as pc
from projman.src.domain.report_generator import ConfidenceInterval, NotAFibonacciEstimateException
from projman.src.domain.repository_collection import RepositoryCollection
import datetime

# ToDos
# - Extract ConfidenceInterval and NotAFibonacciEstimateException to a separate file/module
# - handle no estimate
# - handle not a fibonacci estimate
# - add warnings to MonteCarloSimulationResult
# - normal random selection
# - beta distribution selection

class MonteCarloSimulationResult:
    def __init__(self):
        self.warnings = []
        self.percentiles = {}
        self.bin_edges = []
        self.frequencies = []

class RandomSelector:
    def select(self, interval: ConfidenceInterval) -> float:
        pass

class MonteCarloSimulator:
    def __init__(self, repos: RepositoryCollection, num_simulations: int, random_selector: RandomSelector):
        self.repos = repos
        self.num_simulations = num_simulations
        self.random_selector = random_selector

    def run_simulation(self, start_date: datetime.date) -> MonteCarloSimulationResult:
        velocity, warnings = pc.calculate_recent_velocity(self.repos)

        if velocity is None:
            r = MonteCarloSimulationResult()
            r.warnings = warnings
            return r

        task_repo = self.repos.task_repository
        todo_tasks = list(filter(task.is_todo_task, task_repo.tasks.values()))

        # Todo: repeat this for num_simulations and collect results into histogram
        completion_date = self._run_simulation_iteration(velocity, todo_tasks, start_date)

        result = MonteCarloSimulationResult()
        result.bin_edges = [completion_date]
        result.frequencies = [1]
        return result

    def _run_simulation_iteration(self, velocity: float, todo_tasks: list, start_date: datetime.date) -> datetime.date:
        work_days_sum = 0.0

        for tdt in todo_tasks:
            todoTask: task.Task = tdt
            
            if (not FibonacciSequence.is_in_sequence(todoTask.estimate)):
                    raise NotAFibonacciEstimateException(todoTask.id)

            complexityInterval = ConfidenceInterval(
                FibonacciSequence.predecessor(todoTask.estimate),
                todoTask.estimate,
                FibonacciSequence.successor(todoTask.estimate))

            # Simulate the task completion date based on the complexity interval
            random_complexity = self.random_selector.select(complexityInterval)

            taskDuration = random_complexity / velocity
            work_days_sum += taskDuration

        completion_date = pc.calculate_completion_date(self.repos.working_days_repository_collection, work_days_sum, start_date)

        return completion_date