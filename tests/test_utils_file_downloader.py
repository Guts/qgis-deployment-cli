#! python3  # noqa E265

"""
    Usage from the repo root folder:

    .. code-block:: bash
        # for whole tests
        python -m unittest tests.test_utils_file_downloader
        # for specific test
        python -m unittest tests.test_utils_file_downloader.TestUtilsFileD.test_fd
"""

# standard library
import unittest
from pathlib import Path

# project
from qgis_deployment_toolbelt.utils.file_downloader import download_remote_file_to_local

# ############################################################################
# ########## Classes #############
# ################################


class TestUtilsFileD(unittest.TestCase):
    """Test package utilities."""

    def test_fd(self):
        """Test minimalist download_remote_file_to_local function."""

        # hyphen by default
        self.assertTrue(
            download_remote_file_to_local(
                "https://oslandia.com/wp-content/uploads/2019/11/oslandia_logo_v2_164x154.png",
                Path("../requirements"),
            )
        )


# ############################################################################
# ####### Stand-alone run ########
# ################################
if __name__ == "__main__":
    unittest.main()
