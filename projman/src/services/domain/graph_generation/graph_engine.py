import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from projman.src.services.domain.graph_generation.burndown_graph_generator import BurndownGraphData
from projman.src.domain.monte_carlo_simulator import MonteCarloSimulationResult
from projman.src.services.domain.graph_generation.project_tracking_graph_generator import ProjectTrackingGraphData
from projman.src.services.domain.graph_generation.graph_colors import GraphColorCycle
import datetime

class GraphEngine:

    def plot_burndown_graph(self, data: BurndownGraphData):
        fig, ax = plt.subplots()

        date_formatter = mdates.DateFormatter("%d-%m")
        date_locator = mdates.WeekdayLocator(interval=4)

        ax.set_xlabel("Date")
        ax.xaxis.set_major_formatter(date_formatter)
        ax.xaxis.set_major_locator(date_locator)

        ax.set_ylabel(("Remaining Effort [Story Points]"))

        for free_range in data.free_date_ranges:
            x = [free_range.firstFreeDay, free_range.lastFreeDay + datetime.timedelta(1)]
            ax.fill_between(x, 0, 1, color='blue', alpha=0.3, transform=ax.get_xaxis_transform())

        ax.fill_betweenx(data.lower_confidence_band.y, data.lower_confidence_band.x, data.upper_confidence_band.x, color='gray', alpha=0.3)
        ax.plot(data.lower_confidence_band.x, data.lower_confidence_band.y, '-o', color='gray')
        ax.plot(data.upper_confidence_band.x, data.upper_confidence_band.y, '-o', color='gray')
        ax.plot(data.expected_values.x, data.expected_values.y, '-')
        ax.scatter(data.expected_values.x, data.expected_values.y, c=data.expected_values.color, zorder=2)
        
        plt.show()

    def plot_simulation_historgram(self, data: MonteCarloSimulationResult):
        # plot a bar chart showing frequencies over bin_edges
        fig, ax = plt.subplots()
        ax.bar(data.bin_edges, data.frequencies, align='edge')
        date_formatter = mdates.DateFormatter("%d-%m")
        ax.xaxis.set_major_formatter(date_formatter)
        plt.title("Monte Carlo Simulation Completion Date Histogram")
        ax.set_xlabel("Completion Date")
        ax.set_ylabel("Frequency")
        plt.show()

    def plot_tracking_graph(self, data: ProjectTrackingGraphData):
        fig, ax = plt.subplots()

        plt.title(data.title)

        date_formatter = mdates.DateFormatter("%d-%m")

        ax.set_xlabel("Date")
        ax.xaxis.set_major_formatter(date_formatter)

        ax.set_ylabel("Predicted completion date")
        ax.yaxis.set_major_formatter(date_formatter)

        ax.fill_between(data.lower_confidence_band.x, data.lower_confidence_band.y, data.upper_confidence_band.y, color=GraphColorCycle.Gray, alpha=0.3)
        ax.plot(data.lower_confidence_band.x, data.lower_confidence_band.y, '-o', color=GraphColorCycle.Gray)
        ax.plot(data.upper_confidence_band.x, data.upper_confidence_band.y, '-o', color=GraphColorCycle.Gray)
        ax.plot(data.expected_values.x, data.expected_values.y, '-o', color=GraphColorCycle.Blue, zorder=2)

        plt.show()