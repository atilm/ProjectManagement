import argparse
import os
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

def run_simulation(project: Project, output_directory: str):
    simulation = ProjectSimulation(project, sampler_factory=lambda estimation: BetaSampler(estimation))
    result = simulation.run_simulation(iterations=10000)



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
    
