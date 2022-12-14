import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from src.services.domain.graph_generation.burndown_graph_generator import BurndownGraphData
from src.services.domain.graph_generation.estimation_error_graph_generator import EstimationErrorGraphData
import datetime

class GraphEngine:

    def plot_burndown_graph(self, data: BurndownGraphData):
        fig, ax = plt.subplots()

        date_formatter = mdates.DateFormatter("%d-%m")
        date_locator = mdates.WeekdayLocator(interval=1)

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

    def plot_estimation_error_graph(self, data: EstimationErrorGraphData):
        fig, ax = plt.subplots()

        ax.set_xlabel("Estimation Error [%]")
        ax.set_ylabel("Estimation [Story Points]")

        percentErrors = [e * 100 for e in data.relative_errors.x]
        estimates = data.relative_errors.y

        ax.scatter(percentErrors, estimates, c=data.relative_errors.color, zorder=2)
        ax.grid(axis='x', linestyle='--')

        # ax.vlines(x = 0, ymin = 0, ymax = max(estimates), colors = 'gray',)

        plt.show()