from dependency_monte_carlo.src.project import *

class MermaidFlowDiagramGenerator:
    @staticmethod
    def generate(project: Project) -> str:
        diagram_lines = ["flowchart TD"]
        # Nodes with labels
        for wp in project.work_packages:
            node_label = f"{wp.id}\n    {wp.name}"
            diagram_lines.append(f"    {wp.id}[{node_label}]")

        # Edges based on dependencies
        for wp in project.work_packages:
            for dep in wp.dependencies:
                diagram_lines.append(f"    {dep} --> {wp.id}")

        # Subgraphs: group work packages by 'subgraph' attribute
        subgraph_map = {}
        for wp in project.work_packages:
            name = getattr(wp, 'subgraph', None)
            if name:
                subgraph_map.setdefault(name, []).append(wp.id)

        if subgraph_map:
            # A blank indented line before subgraphs to match expected formatting
            diagram_lines.append("")
            names = list(subgraph_map.keys())
            for idx, name in enumerate(names):
                ids = subgraph_map[name]
                diagram_lines.append(f"    subgraph {name}")
                for wid in ids:
                    diagram_lines.append(f"        {wid}")
                diagram_lines.append("    end")
                # Between subgraphs, use a truly empty line (no spaces)
                if idx < len(names) - 1:
                    diagram_lines.append("")
            # Trailing empty line after the last subgraph
            diagram_lines.append("")

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