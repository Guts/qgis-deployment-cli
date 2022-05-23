#! python3  # noqa E265

"""Usage from the repo root folder:

    .. code-block:: python

        # for whole test
        python -m unittest tests.test_job_profiles_sync
        # for specific
        python -m unittest tests.test_job_profiles_sync.TestJobProfilesSync.test_fresh_install
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import unittest
from os import getenv
from pathlib import Path
from sys import platform as opersys

# package
from qgis_deployment_toolbelt.constants import OS_CONFIG
from qgis_deployment_toolbelt.jobs.job_profiles_synchronizer import (
    JobProfilesDownloader,
)

# #############################################################################
# ########## Classes ###############
# ##################################


class TestJobProfilesSync(unittest.TestCase):
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
    @unittest.skipIf(not getenv("CI", False), "Skip on local machine")
    def test_fresh_install(self):
        """Test QGIS fresh new installation where no profile is installed yet."""
        # variables
        fake_config = {
            "action": "download",
            "source": "https://gitlab.com/Oslandia/qgis/profils_qgis_fr_2022.git",
            "protocol": "git",
            "local_destination": "~/.cache/qgis-deployment-toolbelt/Oslandia/",
            "sync_mode": "overwrite",
        }
        qgis_profiles_path: Path = Path(OS_CONFIG.get(opersys).profiles_path)

        # QGIS profiles folder should not exist yet
        self.assertFalse(qgis_profiles_path.exists())

        # after instanciation, the folder should exist
        profile_manager = JobProfilesDownloader(options=fake_config)
        self.assertTrue(profile_manager.qgis_profiles_path.exists())
