from projman.src.domain.completion_date_history import CompletionDateHistory
from projman.src.services.domain.graph_generation.xy_data import XyData
from projman.src.services.domain.graph_generation.graph_colors import GraphColorCycle

class ProjectTrackingGraphData:
    def __init__(self) -> None:
        self.title: str = ""
        self.lower_confidence_band = XyData()
        self.expected_values = XyData()
        self.upper_confidence_band = XyData()

class ProjectTrackingGraphGenerator:
    def generate(self, history: CompletionDateHistory) -> ProjectTrackingGraphData:
        data = ProjectTrackingGraphData()
        data.title = f"Project: {history.projectId}"

        for record in history.records:
            data.lower_confidence_band.append(record.date, record.completion_date_interval.lower_limit, GraphColorCycle.Gray)
            data.expected_values.append(record.date, record.completion_date_interval.expected_value, GraphColorCycle.Blue)
            data.upper_confidence_band.append(record.date, record.completion_date_interval.upper_limit, GraphColorCycle.Gray)
        
        return data
