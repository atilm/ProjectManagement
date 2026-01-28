from dependency_monte_carlo.src.project import Estimation, Project
import numpy as np
import networkx as nx

class ISampler:
    """Interface for sampling from an estimation distribution."""
    def __init__(self, estimation: Estimation):
        pass

    def sample(self, rng: np.random.Generator) -> float:
        return 0.0

class SimulationWorkPackage:
    """Data set used during simulation of work packages."""
    def __init__(self, work_package, sampler: ISampler):
        self.work_package = work_package
        self.sampler = sampler
        self.simulated_end_times: list[float] = []

    def get_percentile(self, percentile: float) -> float:
        """Get the specified percentile from the simulated end times."""
        if not self.simulated_end_times:
            return 0.0
        return np.percentile(self.simulated_end_times, percentile)

class ProjectSimulationResult:
    """Result of a project simulation."""
    def __init__(self):
        self.total_durations: list[float] = []
        self.work_packages: list[SimulationWorkPackage] = []

    def get_percentile(self, percentile: float) -> float:
        """Get the specified percentile from the simulated end times."""
        if not self.total_durations:
            return 0.0
        return np.percentile(self.total_durations, percentile)

class ProjectSimulation:
    """Monte Carlo Simulator for projects with dependent work packages."""
    def __init__(self, project: Project, sampler_factory):
        self.project = project
        self.sampler_factory = sampler_factory

    def simulate_once(self, dag: nx.DiGraph, rng: np.random.Generator) -> float:
        """Simulate the project once and store results in the graph."""
        # perform topological sort to respect dependencies
        sorted_wps = list(nx.topological_sort(dag))

        earliest_finish = {}
        for work_package_id in sorted_wps:
            work_package: SimulationWorkPackage = dag.nodes[work_package_id]['wp']
            predecessors = list(dag.predecessors(work_package_id))
            start = max((earliest_finish[p] for p in predecessors), default=0.0)
            random_duration = work_package.sampler.sample(rng)
            earliest_finish[work_package_id] = start + random_duration
            work_package.simulated_end_times.append(earliest_finish[work_package_id])
        project_duration = max(earliest_finish.values())
        return project_duration

    def run_simulation(self, iterations: int = 10000) -> ProjectSimulationResult:
        simulation_work_packages = [
            SimulationWorkPackage(wp, self.sampler_factory(wp.estimation))
            for wp in self.project.work_packages
        ]

        # build directed graph of work packages
        dag = nx.DiGraph()
        for wp in simulation_work_packages:
            dag.add_node(wp.work_package.id, wp=wp)
            for p in wp.work_package.dependencies:
                dag.add_edge(p, wp.work_package.id)

        # run simulations with specified number of iterations
        random_state = np.random.default_rng()
        project_durations = []
        for _ in range(iterations):
            project_duration = self.simulate_once(dag, random_state)
            project_durations.append(project_duration)

        result = ProjectSimulationResult()
        result.total_durations = project_durations
        result.work_packages = simulation_work_packages
        return result