import unittest
from dependency_monte_carlo.src.project_yaml_parser import ProjectYamlParser

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
      name: Work pakackge 3
      depends_on: [WP1]
      estimation:
        min: 1
        mode: 5
        max: 10
    - id: WP4
      name: Work pakackge 4
      depends_on: [WP2, WP3]
      estimation:
        min: 0
        mode: 0
        max: 0
"""

class ParserTestCase(unittest.TestCase):
    def test_parse(self):
      import io
      file_obj = io.StringIO(YAML_CONTENT)
      project = ProjectYamlParser.parse(file_obj)

      self.assertEqual(project.name, "My Project")
      self.assertEqual(len(project.work_packages), 4)

      wp1 = project.work_packages[0]
      self.assertEqual(wp1.id, "WP1")
      self.assertEqual(wp1.name, "Work package 1")
      self.assertEqual(wp1.description.strip(), "This is\nwork package 1.")
      self.assertEqual(wp1.dependencies, [])
      self.assertEqual(wp1.estimation.min_val, 5)
      self.assertEqual(wp1.estimation.mode, 14)
      self.assertEqual(wp1.estimation.max_val, 30)

      wp2 = project.work_packages[1]
      self.assertEqual(wp2.id, "WP2")
      self.assertEqual(wp2.dependencies, ["WP1"])
      self.assertEqual(wp2.estimation.min_val, 1)
      self.assertEqual(wp2.estimation.mode, 5)
      self.assertEqual(wp2.estimation.max_val, 10)

      wp3 = project.work_packages[2]
      self.assertEqual(wp3.id, "WP3")
      self.assertEqual(wp3.dependencies, ["WP1"])
      self.assertEqual(wp3.estimation.min_val, 1)
      self.assertEqual(wp3.estimation.mode, 5)
      self.assertEqual(wp3.estimation.max_val, 10)

      wp4 = project.work_packages[3]
      self.assertEqual(wp4.id, "WP4")
      self.assertEqual(wp4.dependencies, ["WP2", "WP3"])
      self.assertEqual(wp4.estimation.min_val, 0)
      self.assertEqual(wp4.estimation.mode, 0)
      self.assertEqual(wp4.estimation.max_val, 0)