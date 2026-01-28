import unittest
from dependency_monte_carlo.src.project import *
from dependency_monte_carlo.src.project_simulation import *
from dependency_monte_carlo.src.project_builder import ProjectBuilder

class ModeSampler(ISampler):
    """A simple sampler that always returns the mode value."""
    def __init__(self, estimation: Estimation):
        self.mode = estimation.mode

    def sample(self, rng: np.random.Generator) -> float:
        return self.mode

def run_simulation(project: Project, num_iterations: int):
    simulation = ProjectSimulation(project, lambda est: ModeSampler(est))
    result = simulation.run_simulation(iterations=num_iterations)
    return result

class SimulationTestCase(unittest.TestCase):
    def test_simulation_runs(self):
        project = ProjectBuilder()\
            .set_name("Test Project")\
            .add_work_package(
                id="WP1",
                name="Work Package 1",
                estimation=Estimation(1, 5, 10)
            )\
            .build()

        num_iterations = 100
        result = run_simulation(project, num_iterations)

        self.assertIsInstance(result, ProjectSimulationResult)
        self.assertEqual(len(result.work_packages), 1)
        wp = result.work_packages[0]
        self.assertEqual(wp.work_package.id, "WP1")
        self.assertEqual(len(wp.simulated_end_times), num_iterations)
        self.assertEqual(wp.simulated_end_times[0], 5)  # Since ModeSampler always returns mode value

    def test_work_package_results_return_percentiles(self):
        project = ProjectBuilder()\
            .set_name("Test Project")\
            .add_work_package(
                id="WP1",
                name="Work Package 1",
                estimation=Estimation(1, 5, 10)
            )\
            .build()
        
        num_iterations = 1000
        result = run_simulation(project, num_iterations)

        wp = result.work_packages[0]
        p = wp.get_percentile(80)
        self.assertEqual(p, 5)  # Since ModeSampler always returns mode value

    def test_project_with_dependencies(self):
        # The dependency graph for the test is:
        #
        #    WP0      WP1
        #     |        |
        #     |        |
        #     |    +---+----+
        #     |    |        |
        #     +---WP2      WP3
        #     |    |        |
        #     +----+--+-----+
        #            |
        #           FIN

        test_cases = [
            # WP0, WP1, WP2, WP3, expected duration
            [1, 1, 1, 1, 2], # Crit path: WP0 -> WP2 -> FIN
            [6, 1, 0, 1, 6], # Crit path: WP0 -> FIN
            [2, 1, 4, 1, 6], # Crit path: WP0 -> WP2 -> FIN
            [1, 5, 2, 1, 7], # Crit path: WP1 -> WP2 -> FIN
            [1, 5, 1, 4, 9], # Crit path: WP1 -> WP3 -> FIN
        ]

        for tc in test_cases:
            project = ProjectBuilder()\
                .set_name("Dependent Project")\
                .add_work_package(
                    id="WP0",
                    name="Work Package 0",
                    estimation=Estimation(0, tc[0], 100)
                )\
                .add_work_package(
                    id="WP1",
                    name="Work Package 1",
                    estimation=Estimation(0, tc[1], 100)
                ).\
                add_work_package(
                    id="WP2",
                    name="Work Package 2",
                    estimation=Estimation(0, tc[2], 100),
                    dependencies=["WP0", "WP1"]
                ).\
                add_work_package(
                    id="WP3",
                    name="Work Package 3",
                    estimation=Estimation(0, tc[3], 100),
                    dependencies=["WP1"]
                ).\
                add_work_package(
                    id="FIN",
                    name="Finish",
                    estimation=Estimation(0, 0, 0),
                    dependencies=["WP0", "WP2", "WP3"]
                )\
                .build()

            num_iterations = 3
            result = run_simulation(project, num_iterations)

            self.assertEqual(len(result.work_packages), 5, f"Failed for test case: {tc}")
            self.assertEqual(result.get_percentile(80), tc[4], f"Failed for test case: {tc}")