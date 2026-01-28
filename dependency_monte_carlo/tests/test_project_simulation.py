import unittest
from dependency_monte_carlo.src.project import *
from dependency_monte_carlo.src.project_simulation import *
from dependency_monte_carlo.src.project_builder import ProjectBuilder

class ModeSampler(ISampler):
    """A simple sampler that always returns the mode value."""
    def __init__(self, estimation: Estimation):
        self.mode = estimation.mode

    def sample(self) -> float:
        return self.mode

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

        simulation = ProjectSimulation(project, lambda est: ModeSampler(est))
        result = simulation.run_simulation(iterations=num_iterations)
        self.assertIsInstance(result, ProjectSimulationResult)
        self.assertEqual(len(result.work_packages), 1)
        wp = result.work_packages[0]

        self.assertEqual(wp.work_package.id, "WP1")
        self.assertEqual(len(wp.simulated_end_times), num_iterations)
        self.assertEqual(wp.simulated_end_times[0], 5)  # Since ModeSampler always returns mode value
        