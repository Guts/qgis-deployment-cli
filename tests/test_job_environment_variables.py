#! python3  # noqa E265

"""Usage from the repo root folder:

    .. code-block:: python

        # for whole test
        python -m unittest tests.test_job_environment_variables
        # for specific
        python -m unittest tests.test_job_environment_variables.TestJobEnvironmentVariables.test_environment_variables_set
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import unittest
from os.path import expanduser
from pathlib import Path
from sys import platform as opersys

# package
from qgis_deployment_toolbelt.jobs.job_environment_variables import (
    JobEnvironmentVariables,
)
from qgis_deployment_toolbelt.utils import str2bool

if opersys == "win32":
    from qgis_deployment_toolbelt.utils.win32utils import get_environment_variable

# #############################################################################
# ########## Classes ###############
# ##################################


class TestJobEnvironmentVariables(unittest.TestCase):
    """Test module."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        cls.good_scenario_files = sorted(
            Path("tests/fixtures/").glob("scenarios/good_*.y*ml")
        )

    # standard methods
    def setUp(self):
        """Fixtures prepared before each test."""
        pass

    def tearDown(self):
        """Executed after each test."""
        pass

    # -- TESTS ---------------------------------------------------------
    @unittest.skipIf(opersys != "win32", "Test specific to Windows.")
    def test_environment_variables_set(self):
        """Test YAML loader"""
        fake_env_vars = [
            {
                "name": "QDT_TEST_FAKE_ENV_VAR_BOOL",
                "value": True,
                "scope": "user",
                "action": "add",
            },
            {
                "name": "QDT_TEST_FAKE_ENV_VAR_PATH",
                "value": "~/scripts/qgis_startup.py",
                "scope": "user",
                "action": "add",
            },
        ]
        job_env_vars = JobEnvironmentVariables(fake_env_vars)
        job_env_vars.run()

        # check if environment variables have been set
        if opersys == "win32":
            self.assertTrue(
                str2bool(
                    get_environment_variable("QDT_TEST_FAKE_ENV_VAR_BOOL", "user")
                ),
                True,
            )
            self.assertEqual(
                get_environment_variable("QDT_TEST_FAKE_ENV_VAR_PATH"),
                str(Path(expanduser("~/scripts/qgis_startup.py")).resolve()),
            )
