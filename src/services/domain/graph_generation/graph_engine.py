import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from src.services.domain.graph_generation.burndown_graph_generator import BurndownGraphData
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
