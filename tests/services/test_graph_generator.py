from tests.domain.domain_test_case import DomainTestCase
from src.services.domain.graph_generation.xy_data import XyData

class GraphGeneratorTestCase(DomainTestCase):
    def assert_xy_data(self, xy_data: XyData, expected_x: list, expected_y: list):
        self.assertEqual(xy_data.x, expected_x)
        self.assertEqual(xy_data.y, expected_y)
