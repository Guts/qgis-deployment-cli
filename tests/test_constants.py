#! python3  # noqa E265

"""
    Usage from the repo root folder:

    .. code-block:: bash
        # for whole tests
        python -m unittest tests.test_constants
        # for specific test
        python -m unittest tests.test_constants.TestConstants.test_constants
"""

# standard library
import unittest
from pathlib import Path
from sys import platform as opersys

# project
from qgis_deployment_toolbelt import constants

# ############################################################################
# ########## Classes #############
# ################################


class TestConstants(unittest.TestCase):
    """Test package static variables."""

    def test_constants(self):
        """Test types."""
        self.assertIsInstance(constants.OS_CONFIG, dict)
        os_config = constants.OS_CONFIG.get(opersys)
        self.assertIsInstance(os_config, constants.OSConfiguration)

        self.assertIsInstance(os_config.profiles_path, Path)
        self.assertIsInstance(os_config.shortcut_extension, str)
        self.assertIsInstance(os_config.shortcut_forbidden_chars, tuple)
        self.assertIsInstance(os_config.shortcut_icon_extensions, tuple)


# ############################################################################
# ####### Stand-alone run ########
# ################################
if __name__ == "__main__":
    unittest.main()
