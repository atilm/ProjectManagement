from dependency_monte_carlo.src.project_simulation import ProjectSimulationResult
from dependency_monte_carlo.src.project import Project
import datetime

class MermaidGanttDiagramGenerator:
    @staticmethod
    def generate(project_simulation_result: ProjectSimulationResult, project_name: str, start_date: datetime.date, percentile: float=85) -> str:
        diagram_lines = [
            f"gantt",
            f'    title {project_name} Gantt Chart',
            # f'    axisFormat  %d',
            f'    dateFormat  DD-MM-YYYY']
        
        simulation_work_packages_by_id = {swp.work_package.id: swp for swp in project_simulation_result.work_packages}

        for swp in simulation_work_packages_by_id.values():
            # get end date at specified percentile
            end_time = swp.get_percentile(percentile)
            end_date = start_date + datetime.timedelta(days=end_time)

            # get start date as the maximum end date of dependencies
            start_time = 0.0
            if swp.work_package.dependencies:
                dependencies_end_times = []
                for dep_id in swp.work_package.dependencies:
                    if dep_id in simulation_work_packages_by_id:
                        dep_swp = simulation_work_packages_by_id[dep_id]
                        dep_end_time = dep_swp.get_percentile(percentile)
                        dependencies_end_times.append(dep_end_time)
                if dependencies_end_times:
                    start_time = max(dependencies_end_times)
            start_date_wp = start_date + datetime.timedelta(days=start_time)

            # add line to diagram
            diagram_lines.append(f'    {swp.work_package.id} {swp.work_package.name} :{swp.work_package.id}, {start_date_wp.strftime("%d-%m-%Y")}, {end_date.strftime("%d-%m-%Y")}')
        
        return "\n".join(diagram_lines)