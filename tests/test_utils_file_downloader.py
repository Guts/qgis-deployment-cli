#! python3  # noqa E265

"""
    Usage from the repo root folder:

    .. code-block:: bash
        # for whole tests
        python -m unittest tests.test_utils_file_downloader
        # for specific test
        python -m unittest tests.test_utils_file_downloader.TestUtilsFileDownloader.test_download_file_exists
"""

# standard library
import tempfile
import unittest
from pathlib import Path

# 3rd party
from requests.exceptions import ConnectionError, HTTPError

# project
from qgis_deployment_toolbelt.utils.file_downloader import download_remote_file_to_local

# ############################################################################
# ########## Classes #############
# ################################


class TestUtilsFileDownloader(unittest.TestCase):
    """Test package utilities."""

    def test_download_file_exists(self):
        """Test download remote file locally to a file which already exists."""
        with tempfile.TemporaryDirectory(
            prefix="qdt_test_downloader_", ignore_cleanup_errors=True
        ) as tmpdirname:
            # file that already exist locally
            downloaded_file = download_remote_file_to_local(
                remote_url_to_download="https://raw.githubusercontent.com/Guts/qgis-deployment-cli/main/README.md",
                local_file_path=Path(tmpdirname).joinpath("README_from_remote.md"),
            )
            self.assertIsInstance(downloaded_file, Path)
            self.assertTrue(downloaded_file.exists())
            self.assertTrue(downloaded_file.is_file())

    def test_download_file_raise_http_error(self):
        """Test download handling an HTTP error."""
        with tempfile.TemporaryDirectory(
            prefix="qdt_test_downloader_", ignore_cleanup_errors=True
        ) as tmpdirname:
            target_path = Path(tmpdirname).joinpath("dl_404.html")
            with self.assertRaises(HTTPError):
                download_remote_file_to_local(
                    remote_url_to_download="https://qgis.org/fake-page",
                    local_file_path=target_path,
                )
            self.assertFalse(target_path.exists())
            self.assertFalse(target_path.is_file())

    def test_download_file_raise_url_error(self):
        """Test download with a bad URL."""
        with tempfile.TemporaryDirectory(
            prefix="qdt_test_downloader_", ignore_cleanup_errors=True
        ) as tmpdirname:
            target_path = Path(tmpdirname).joinpath("fake_file.dmg")
            with self.assertRaises(ConnectionError):
                download_remote_file_to_local(
                    remote_url_to_download="https://fake_url/youpi.dmg",
                    local_file_path=target_path,
                )
            self.assertFalse(target_path.exists())
            self.assertFalse(target_path.is_file())


# ############################################################################
# ####### Stand-alone run ########
# ################################
if __name__ == "__main__":
    unittest.main()
