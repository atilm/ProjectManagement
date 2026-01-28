import argparse
import os
import datetime
import matplotlib.pyplot as plt
from dependency_monte_carlo.src.project_yaml_parser import ProjectYamlParser
from dependency_monte_carlo.src.flow_diagram_generator import MermaidFlowDiagramGenerator
from dependency_monte_carlo.src.project import Project
from dependency_monte_carlo.src.project_simulation import ProjectSimulation, BetaSampler

def generate_dependency_diagram(project: Project, directory: str):
    diagram_content = MermaidFlowDiagramGenerator.generate(project)
    work_package_descriptions = MermaidFlowDiagramGenerator.generate_markdown_descriptions(project)
    output_file_path = os.path.join(directory, "project_dependencies.md")
    with open(output_file_path, 'w') as output_file:
        output_file.write(f"""# Project Dependencies Diagram
```mermaid
{diagram_content}
```

{work_package_descriptions}
        """)

def generate_gantt_diagram(project_simulation_result, project_name: str, start_date: datetime.date, output_directory: str):
    from dependency_monte_carlo.src.gantt_diagram_generator import MermaidGanttDiagramGenerator

    diagram_content = MermaidGanttDiagramGenerator.generate(
        project_simulation_result,
        project_name,
        start_date,
        percentile=85
    )
    output_file_path = os.path.join(output_directory, "project_gantt_diagram.md")
    with open(output_file_path, 'w') as output_file:
        output_file.write(f"""# Project Gantt Diagram
```mermaid
{diagram_content}
```
        """)

def run_simulation(project: Project, output_directory: str):
    simulation = ProjectSimulation(project, sampler_factory=lambda estimation: BetaSampler(estimation))
    result = simulation.run_simulation(iterations=10000)

    generate_gantt_diagram(
        result,
        project.name,
        datetime.date.today(),
        output_directory
    )

    project_durations_in_days = result.total_durations
    now = datetime.datetime.now()
    project_end_dates_from_today = [now + datetime.timedelta(days=duration) for duration in project_durations_in_days]
    ordinals = [date.toordinal() for date in project_end_dates_from_today]
    plt.hist(ordinals, bins=30, edgecolor='black')
    plt.xlabel('Completion Date')
    plt.ylabel('Frequency')
    plt.title(f'Forecasted Completion Dates for the project')
    locs, labels = plt.xticks()
    plt.xticks(locs, [datetime.datetime.fromordinal(int(l)).strftime('%Y-%m-%d') for l in locs], rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, 'project_completion_forecast.png'))
    plt.close()


if __name__ == "__main__":
    argumentParser = argparse.ArgumentParser(prog="monte-carlo-dependencies", description="Cli project management tools")
    argumentParser.add_argument("project_file_path", help="Path to the project YAML file")
    
    args = argumentParser.parse_args()
    project_file_path = args.project_file_path

    directory = os.path.dirname(project_file_path)

    print(f"Project file path: {project_file_path}")

    project = ProjectYamlParser.parse(open(project_file_path, 'r'))

    generate_dependency_diagram(project, directory)
    run_simulation(project, directory)
    
