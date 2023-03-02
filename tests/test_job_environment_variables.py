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

# package
from qgis_deployment_toolbelt.jobs.job_environment_variables import (
    JobEnvironmentVariables,
)
from qgis_deployment_toolbelt.utils import str2bool

if opersys == "win32":
    import platform

    from qgis_deployment_toolbelt.utils.win32utils import (  # delete_environment_variable,
        get_environment_variable,
    )

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
    def test_environment_variables_set_unset(self):
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

            # clean up
            fake_env_vars = [
                {
                    "name": "QDT_TEST_FAKE_ENV_VAR_BOOL",
                    "scope": "user",
                    "action": "remove",
                },
                {
                    "name": "QDT_TEST_FAKE_ENV_VAR_PATH",
                    "scope": "user",
                    "action": "remove",
                },
            ]
            job_env_vars = JobEnvironmentVariables(fake_env_vars)
            job_env_vars.run()

            self.assertIsNone(
                get_environment_variable("QDT_TEST_FAKE_ENV_VAR_BOOL", "user")
            )
            self.assertIsNone(
                get_environment_variable("QDT_TEST_FAKE_ENV_VAR_PATH"),
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
            self.assertEqual(
                job_env_vars.prepare_value(value=value_test),
                str(Path().resolve() / value_test),
            )
            self.assertEqual(
                job_env_vars.prepare_value(value=[]),
                "[]",
            )
        else:
            self.assertEqual(
                job_env_vars.prepare_value(value=value_test),
                str(Path().resolve() / value_test),
            )
            self.assertEqual(
                job_env_vars.prepare_value(value=[]),
                "[]",
            )

    def test_validate_options(self):
        """Test validate_options method"""
        job_env_vars = JobEnvironmentVariables([])
        # Options must be a dictionary
        with self.assertRaises(ValueError):
            job_env_vars.validate_options(options="options_test")
        with self.assertRaises(ValueError):
            job_env_vars.validate_options(options=["options_test"])

        bad_options_scope = [
            {
                "action": "remove",
                "name": "QDT_TEST_FAKE_ENV_VAR_BOOL",
                "scope": "imaginary_scope",
            }
        ]
        bad_options_action = [
            {
                "action": "update",
                "name": "QDT_TEST_FAKE_ENV_VAR_PATH",
                "scope": "user",
            },
        ]

        with self.assertRaises(ValueError):
            JobEnvironmentVariables(bad_options_action)
        with self.assertRaises(ValueError):
            JobEnvironmentVariables(bad_options_scope)
