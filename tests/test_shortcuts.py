#! python3  # noqa E265

"""
    Usage from the repo root folder:

    .. code-block:: bash
        # for whole tests
        python -m unittest tests.test_shortcuts
        # for specific test
        python -m unittest tests.test_shortcuts.TestShortcut.test_shortcut_creation
"""

import unittest
from pathlib import Path
from sys import platform as opersys

# project
from qgis_deployment_toolbelt.profiles.shortcuts import ApplicationShortcut

# ############################################################################
# ########## Classes #############
# ################################


class TestShortcut(unittest.TestCase):
    """Test shortcut creation and deletion."""

    def test_shortcut_creation_complete(self):
        """Test creation of shortcut."""
        shortcut = ApplicationShortcut(
            name="test shortcut",
            description="A test shortcut",
            exec_path=Path(__file__),
            exec_arguments=("--test", "unit"),
            work_dir=Path(__file__).parent,
            icon_path=Path(__file__).parent / "icon.png",
        )

        shortcuts_paths = shortcut.create(
            desktop=True,
            start_menu=True,
        )

        if opersys == "win32":
            self.assertIsInstance(shortcuts_paths, tuple)


# ############################################################################
# ####### Stand-alone run ########
# ################################
if __name__ == "__main__":
    unittest.main()
