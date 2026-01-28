from dependency_monte_carlo.src.project import Estimation, Project

class ISampler:
    """Interface for sampling from an estimation distribution."""
    def __init__(self, estimation: Estimation):
        pass

    def sample(self) -> float:
        return 0.0

class SimulationWorkPackage:
    """Data set used during simulation of work packages."""
    def __init__(self, work_package, sampler: ISampler):
        self.work_package = work_package
        self.sampler = sampler
        self.simulated_end_times: list[float] = []

class ProjectSimulationResult:
    """Result of a project simulation."""
    def __init__(self):
        self.total_duration: float = 0.0
        self.work_packages: list[SimulationWorkPackage] = []

class ProjectSimulation:
    """Monte Carlo Simulator for projects with dependent work packages."""
    def __init__(self, project: Project, sampler_factory):
        self.project = project
        self.sampler_factory = sampler_factory

    def run_simulation(self, iterations: int = 10000) -> ProjectSimulationResult:
        simulation_work_packages = [
            SimulationWorkPackage(wp, self.sampler_factory(wp.estimation))
            for wp in self.project.work_packages
        ]

        for _ in range(iterations):
            for sim_wp in simulation_work_packages:
                sampled_duration = sim_wp.sampler.sample()
                sim_wp.simulated_end_times.append(sampled_duration)

        result = ProjectSimulationResult()
        result.work_packages = simulation_work_packages
        # Placeholder for simulation logic
        return result