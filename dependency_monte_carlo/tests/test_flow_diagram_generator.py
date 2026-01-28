import unittest
from dependency_monte_carlo.src.project_yaml_parser import ProjectYamlParser
from dependency_monte_carlo.src.flow_diagram_generator import MermaidFlowDiagramGenerator
from dependency_monte_carlo.src.project import Project

YAML_CONTENT = """
project:
  name: My Project
  work_packages:
    - id: WP1
      name: Work package 1
      description: |
        This is
        work package 1.
      depends_on: []
      estimation:
        min: 5
        mode: 14
        max: 30
    - id: WP2
      name: Work package 2
      depends_on: [WP1]
      estimation:
        min: 1
        mode: 5
        max: 10
    - id: WP3
      name: Work package 3
      depends_on: [WP1]
      estimation:
        min: 1
        mode: 5
        max: 10
    - id: WP4
      name: Work package 4
      depends_on: [WP2, WP3]
      estimation:
        min: 0
        mode: 0
        max: 0
"""

class FlowDiagramGeneratorTestCase(unittest.TestCase):
    def test_generate(self):
        import io
        file_obj = io.StringIO(YAML_CONTENT)
        project = ProjectYamlParser.parse(file_obj)

        diagram = MermaidFlowDiagramGenerator.generate(project)

        expected_diagram = """flowchart TD
    WP1[WP1
    Work package 1]
    WP2[WP2
    Work package 2]
    WP3[WP3
    Work package 3]
    WP4[WP4
    Work package 4]
    WP1 --> WP2
    WP1 --> WP3
    WP2 --> WP4
    WP3 --> WP4"""

        self.assertEqual(diagram.strip(), expected_diagram.strip())