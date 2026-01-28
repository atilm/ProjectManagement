from dependency_monte_carlo.src.project import *

class MermaidFlowDiagramGenerator:
    @staticmethod
    def generate(project: Project) -> str:
        diagram_lines = ["flowchart TD"]
        for wp in project.work_packages:
            node_label = f"{wp.id}\n    {wp.name}"
            diagram_lines.append(f"    {wp.id}[{node_label}]")
        for wp in project.work_packages:
            for dep in wp.dependencies:
                diagram_lines.append(f"    {dep} --> {wp.id}")
        return "\n".join(diagram_lines)
    
    @staticmethod
    def generate_markdown_descriptions(project: Project) -> str:
        md_lines = []
        for wp in project.work_packages:
            if not(wp.description):
                continue

            md_lines.append(f"## {wp.id}: {wp.name}")
            md_lines.append(f"{wp.description}")

        return "\n".join(md_lines)