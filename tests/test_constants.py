#! python3  # noqa E265

"""
    Usage from the repo root folder:

    .. code-block:: bash
        # for whole tests
        python -m unittest tests.test_constants
        # for specific test
        python -m unittest tests.test_constants.TestConstants.test_constants
"""

import unittest
from os import environ, getenv, unsetenv
from os.path import expanduser, expandvars
from pathlib import Path
from sys import platform as opersys

# project
from qgis_deployment_toolbelt import constants

# ############################################################################
# ########## Classes #############
# ################################


class TestConstants(unittest.TestCase):
    """Test package static variables."""

    def setUp(self) -> None:
        if "QDT_QGIS_EXE_PATH" in environ or getenv("QDT_QGIS_EXE_PATH"):
            unsetenv("QDT_QGIS_EXE_PATH")
            environ.pop("QDT_QGIS_EXE_PATH")

    def test_constants(self):
        """Test types."""
        self.assertIsInstance(constants.OS_CONFIG, dict)
        os_config = constants.OS_CONFIG.get(opersys)
        self.assertIsInstance(os_config, constants.OSConfiguration)

        self.assertIsInstance(os_config.profiles_path, Path)
        self.assertIsInstance(os_config.shortcut_extension, str)
        self.assertIsInstance(os_config.shortcut_forbidden_chars, (tuple, type(None)))
        self.assertIsInstance(os_config.shortcut_icon_extensions, tuple)

        # Check for forbidden characters in the shortcut name
        os_config_forbidden_chars = constants.OSConfiguration(
            name_python=opersys, shortcut_forbidden_chars=(" ", "-")
        )
        self.assertFalse(
            os_config_forbidden_chars.valid_shortcut_name(shortcut_name="qgis-ltr 3.28")
        )
        self.assertTrue(
            os_config_forbidden_chars.valid_shortcut_name(shortcut_name="qgis_ltr_3_28")
        )

    def test_get_qdt_working_folder(self):
        """Test how QDT working folder is retrieved"""
        # using specific value
        self.assertEqual(
            constants.get_qdt_working_directory(
                specific_value="~/.cache/qdt/unit-tests/"
            ),
            Path(Path.home(), ".cache/qdt/unit-tests/"),
        )

        # using environment variable
        environ["QDT_LOCAL_WORK_DIR"] = "~/.cache/qdt/unit-tests-env-var/"
        self.assertEqual(
            constants.get_qdt_working_directory(),
            Path(Path.home(), ".cache/qdt/unit-tests-env-var/"),
        )
        unsetenv("QDT_LOCAL_WORK_DIR")

    def test_get_qgis_bin_path(self):
        """Test get GIS exe path helper property"""
        os_config: constants.OS_CONFIG = constants.OS_CONFIG.get(opersys)
        # default value
        self.assertEqual(os_config.get_qgis_bin_path, os_config.qgis_bin_exe_path)

    def test_get_qgis_bin_path_with_env_var_str(self):
        """Test with environment var set as str"""
        if "QDT_QGIS_EXE_PATH" in environ:
            environ.pop("QDT_QGIS_EXE_PATH")
        environ["QDT_QGIS_EXE_PATH"] = "/usr/bin/toto"
        os_config: constants.OS_CONFIG = constants.OS_CONFIG.get(opersys)
        self.assertEqual(os_config.get_qgis_bin_path, Path("/usr/bin/toto"))

        environ.pop("QDT_QGIS_EXE_PATH")
        environ["QDT_QGIS_EXE_PATH"] = "~/qgis-ltr-bin.exe"
        os_config: constants.OS_CONFIG = constants.OS_CONFIG.get(opersys)
        self.assertEqual(
            os_config.get_qgis_bin_path,
            Path(expanduser("~/qgis-ltr-bin.exe")).resolve(),
        )

        environ.pop("QDT_QGIS_EXE_PATH")

    def test_get_qgis_bin_path_with_env_var_dict(self):
        """Test get GIS exe path helper property"""
        if "QDT_QGIS_EXE_PATH" in environ:
            environ.pop("QDT_QGIS_EXE_PATH")
        # with environment var set as dict
        d_test = {
            "linux": "/usr/bin/qgis",
            "darwin": "/usr/bin/qgis",
            "win32": "%PROGRAMFILES%/QGIS/3_22/bin/qgis-ltr-bin.exe",
        }
        environ["QDT_QGIS_EXE_PATH"] = str(d_test)

        os_config: constants.OS_CONFIG = constants.OS_CONFIG.get(opersys)

        self.assertEqual(
            os_config.get_qgis_bin_path,
            Path(expandvars(expanduser(d_test.get(opersys)))),
        )

        environ.pop("QDT_QGIS_EXE_PATH")


# ############################################################################
# ####### Stand-alone run ########
# ################################
if __name__ == "__main__":
    unittest.main()
