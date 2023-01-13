#! python3  # noqa E265

"""Usage from the repo root folder:

    .. code-block:: python

        # for whole test
        python -m unittest tests.test_job_environment_variables
        # for specific
        python -m unittest tests.test_job_environment_variables.TestJobsLaunch.test_jobs_launcher
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import unittest
from os.path import expanduser
from pathlib import Path
from sys import platform as opersys
from unittest import mock

# package
from qgis_deployment_toolbelt.jobs.job_environment_variables import (
    JobEnvironmentVariables,
)
from qgis_deployment_toolbelt.utils import str2bool

if opersys == "win32":
    import platform

    from qgis_deployment_toolbelt.utils.win32utils import get_environment_variable

    PYTHON_RELEASE = platform.python_version()


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

    def test_prepare_value(self):
        """Test prepare_value method"""
        job_env_vars = JobEnvironmentVariables([])
        value_test = f"tests/{Path(__file__).name}"
        self.assertEqual(
            job_env_vars.prepare_value(value=value_test),
            str(Path().resolve() / value_test),
        )
        value_test = "imaginary/path"
        if opersys == "win32":
            if PYTHON_RELEASE.startswith(("3.8", "3.9")):
                self.assertEqual(
                    job_env_vars.prepare_value(value=value_test),
                    value_test.replace("/", "\\"),
                )
                self.assertEqual(
                    job_env_vars.prepare_value(value=[]),
                    [],
                )
            else:
                self.assertEqual(
                    job_env_vars.prepare_value(value=value_test),
                    str(Path().resolve() / value_test),
                )
                self.assertEqual(
                    job_env_vars.prepare_value(value=[]),
                    [],
                )
        else:
            self.assertEqual(
                job_env_vars.prepare_value(value=value_test),
                str(Path().resolve() / value_test),
            )
            self.assertEqual(
                job_env_vars.prepare_value(value=[]),
                '"[]"',
            )

    def test_validate_options(self):
        """Test validate_options method"""
        job_env_vars = JobEnvironmentVariables([])
        # Options must be a list of dictionaries
        with self.assertRaises(TypeError):
            job_env_vars.validate_options(options="options_test")
        with self.assertRaises(TypeError):
            job_env_vars.validate_options(options=["options_test"])


# simulate an opersys variable equal to win32
@mock.patch("qgis_deployment_toolbelt.jobs.job_environment_variables.opersys", "win32")
class TestJobEnvironmentVariablesImaginaryOpersysWin32(unittest.TestCase):
    """Test module with a fake opersys variable equal to win32"""

    def test_run(self):
        """Test run method"""
        job_env_vars = JobEnvironmentVariables(
            [
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
                    "action": "add_test",
                },
            ]
        )
        self.assertIsNone(job_env_vars.run())

    def test_prepare_value(self):
        """Test prepare_value method"""
        job_env_vars = JobEnvironmentVariables([])
        self.assertEqual(job_env_vars.prepare_value(value=[]), [])
