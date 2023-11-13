#! python3  # noqa E265

"""
    Usage from the repo root folder:

    .. code-block:: bash
        # for whole tests
        python -m unittest tests.test_qgis_ini_helper
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

        self.assertEqual(ini_config.ini_type, "profile_qgis3")
        self.assertFalse(ini_config.is_ui_customization_enabled())

    def test_load_profile_customization_splash_screen(self):
        """Test profile QGIS/QGIS3.ini loader."""
        new_config_file = Path(
            "tests/fixtures/qgis_ini/default_customization/QGISCUSTOMIZATION3.ini"
        )
        ini_customization = QgisIniHelper(ini_filepath=new_config_file)

        self.assertEqual(ini_customization.ini_type, "profile_qgis3customization")

        ini_config = QgisIniHelper(ini_filepath=ini_customization.profile_config_path)

        self.assertEqual(ini_config.ini_type, "profile_qgis3")

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

    def test_enable_customization_on_unexisting_file(self):
        """Test profile QGIS/QGIS3.ini loader."""
        unexisting_config_file = Path("Imaginary_QGIS3.ini")
        self.assertFalse(unexisting_config_file.exists())
        ini_config = QgisIniHelper(
            ini_filepath=unexisting_config_file, ini_type="profile_qgis3"
        )
        self.assertFalse(ini_config.is_ui_customization_enabled())
        self.assertFalse(unexisting_config_file.exists())

        ini_config.set_ui_customization_enabled(switch=True)
        self.assertTrue(ini_config.is_ui_customization_enabled())
        self.assertTrue(unexisting_config_file.exists())

        ini_config.set_ui_customization_enabled(switch=False)
        self.assertFalse(ini_config.is_ui_customization_enabled())
        self.assertTrue(unexisting_config_file.exists())

        unexisting_config_file.unlink(missing_ok=True)

    def test_splash_already_set(self):
        fake_config = (
            "[Customization]\nsplashpath=/home/$USER/.share/QGIS/QGIS3/images/"
        )

        tmp_ini_customization = Path(
            "tests/fixtures/tmp/customization_with_splashpath.ini"
        )
        tmp_ini_customization.parent.mkdir(parents=True, exist_ok=True)
        tmp_ini_customization.write_text(fake_config)

        qini_helper = QgisIniHelper(
            ini_filepath=tmp_ini_customization, ini_type="profile_qgis3customization"
        )
        self.assertTrue(qini_helper.is_splash_screen_set())

        tmp_ini_customization.unlink()

    def test_splash_already_set_but_empty(self):
        fake_config = "[Customization]\nsplashpath="

        tmp_ini_customization = Path(
            "tests/fixtures/tmp/customization_with_splashpath_empty.ini"
        )
        tmp_ini_customization.parent.mkdir(parents=True, exist_ok=True)
        tmp_ini_customization.write_text(fake_config)

        qini_helper = QgisIniHelper(
            ini_filepath=tmp_ini_customization, ini_type="profile_qgis3customization"
        )
        self.assertFalse(qini_helper.is_splash_screen_set())

        tmp_ini_customization.unlink()

    def test_splash_not_set(self):
        fake_config = "[Customization]\nMenu\\mDatabaseMenu=false"

        tmp_ini_customization = Path(
            "tests/fixtures/tmp/customization_with_no_splashpath_set.ini"
        )
        tmp_ini_customization.parent.mkdir(parents=True, exist_ok=True)
        tmp_ini_customization.write_text(fake_config)

        qini_helper = QgisIniHelper(
            ini_filepath=tmp_ini_customization, ini_type="profile_qgis3customization"
        )
        self.assertFalse(qini_helper.is_splash_screen_set())

        tmp_ini_customization.unlink()

    def test_disable_splash_already_not_set(self):
        fake_config = "[Customization]\nMenu\\mDatabaseMenu=false"

        tmp_ini_customization = Path(
            "tests/fixtures/tmp/set_splash_path_on_customization_with_no_splashpath_set.ini"
        )
        tmp_ini_customization.parent.mkdir(parents=True, exist_ok=True)
        tmp_ini_customization.write_text(fake_config)

        qini_helper = QgisIniHelper(
            ini_filepath=tmp_ini_customization, ini_type="profile_qgis3customization"
        )
        self.assertFalse(qini_helper.set_splash_screen(switch=False))

        tmp_ini_customization.unlink()

    def test_disable_splash_on_unexisting_file(self):
        not_existing_ini_customization = Path("not_existing_customization.ini")

        qini_helper = QgisIniHelper(
            ini_filepath=not_existing_ini_customization,
            ini_type="profile_qgis3customization",
        )
        self.assertFalse(qini_helper.set_splash_screen(switch=False))

        not_existing_ini_config = Path("QGIS3.ini")

        qini_helper = QgisIniHelper(
            ini_filepath=not_existing_ini_config, ini_type="profile_qgis3"
        )
        self.assertFalse(qini_helper.set_splash_screen(switch=False))


# ############################################################################
# ####### Stand-alone run ########
# ################################
if __name__ == "__main__":
    unittest.main()
