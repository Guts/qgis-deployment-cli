#! python3  # noqa E265

"""Usage from the repo root folder:

    .. code-block:: python

        # for whole test
        python -m unittest tests.test_scenario_reader
        # for specific
        python -m unittest tests.test_scenario_reader.TestScenarioReader.test_load_from_yaml
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import unittest
from pathlib import Path

# module target
from qgis_deployment_toolbelt.scenarios.scenario_reader import ScenarioReader

# #############################################################################
# ########## Classes ###############
# ##################################


class TestScenarioReader(unittest.TestCase):
    """Test module."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        cls.good_scenario_files = sorted(Path("tests/fixtures/").glob("good_*.y*ml"))

    # standard methods
    def setUp(self):
        """Fixtures prepared before each test."""
        pass

    def tearDown(self):
        """Executed after each test."""
        pass

    # -- TESTS ---------------------------------------------------------
    def test_load_from_yaml(self):
        """Test YAML loader"""
        for i in self.good_scenario_files:
            reader = ScenarioReader(in_yaml=i)
            self.assertIsInstance(reader.yaml_data, dict)
            self.assertIn("title", reader.yaml_data)
            self.assertIn("environment_variables", reader.yaml_data)
            self.assertIn("steps", reader.yaml_data)
