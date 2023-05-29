#! python3  # noqa E265

"""
    Usage from the repo root folder:

    .. code-block:: bash
        # for whole tests
        python -m unittest tests.test_qdt_profile_object
        # for specific test
        python -m unittest tests.test_qgis_ini_helper.TestQgisIniHelper.test_profile_load_from_json_basic
"""

# standard
import unittest
from pathlib import Path

# project
from qgis_deployment_toolbelt.profiles.qgis_ini_handler import QgisIniHelper

# ############################################################################
# ########## Classes #############
# ################################


class TestQgisIniHelper(unittest.TestCase):
    """Test module handling QGIS configuration files (*.ini)."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        cls.configuration_files = sorted(Path("tests/fixtures/").glob("**/QGIS3*.ini"))
        cls.customization_files = sorted(Path("tests/fixtures/").glob("**/QGIS3*.ini"))

    def test_load_profile_config_default(self):
        """Test profile QGIS/QGIS3.ini loader."""
        new_config_file = Path(
            "tests/fixtures/qgis_ini/default_no_customization/QGIS3.ini"
        )
        ini_config = QgisIniHelper(ini_filepath=new_config_file)

        self.assertEqual(ini_config.INI_TYPE, "profile_qgis3")
        self.assertFalse(ini_config.is_ui_customization_enabled())

    def test_load_profile_customization_splash_screen(self):
        """Test profile QGIS/QGIS3.ini loader."""
        new_config_file = Path(
            "tests/fixtures/qgis_ini/default_customization/QGISCUSTOMIZATION3.ini"
        )
        ini_customization = QgisIniHelper(ini_filepath=new_config_file)

        self.assertEqual(ini_customization.INI_TYPE, "profile_qgis3customization")

        ini_config = QgisIniHelper(ini_filepath=ini_customization.profile_config_path)

        self.assertEqual(ini_config.INI_TYPE, "profile_qgis3")

    def test_enable_customization(self):
        """Test profile QGIS/QGIS3.ini loader."""
        new_config_file = Path(
            "tests/fixtures/qgis_ini/default_no_customization/QGIS3.ini"
        )
        ini_config = QgisIniHelper(ini_filepath=new_config_file)
        self.assertFalse(ini_config.is_ui_customization_enabled())

        ini_config.set_ui_customization_enabled(switch=True)
        self.assertTrue(ini_config.is_ui_customization_enabled())

        ini_config.set_ui_customization_enabled(switch=False)
        self.assertFalse(ini_config.is_ui_customization_enabled())


# ############################################################################
# ####### Stand-alone run ########
# ################################
if __name__ == "__main__":
    unittest.main()
