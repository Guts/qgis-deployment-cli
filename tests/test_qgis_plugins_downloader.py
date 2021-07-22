#! python3  # noqa E265

"""
    Usage from the repo root folder:

    .. code-block:: bash
        # for whole tests
        python -m unittest tests.test_plg_metadata
        # for specific test
        python -m unittest tests.test_plg_metadata.TestPluginMetadata.test_version_semver
"""

# standard library
import unittest

# project
from qgis_deployment_toolbelt.plugins.plugin_downloader import QgisPluginsDownloader

# ############################################################################
# ########## Classes #############
# ################################


class TestPluginsDownloader(unittest.TestCase):
    def test_repository_type(self):
        """Test repository type guesser."""
        # local file
        plg_downloader = QgisPluginsDownloader(
            min_qgis_version="3.16",
            repository_source="tests/fixtures/plugins_316_test.xml",
        )
        self.assertTrue(plg_downloader.repository_type, "local_file")

        # local folder
        plg_downloader = QgisPluginsDownloader(
            min_qgis_version="3.16",
            repository_source="tests/fixtures/",
        )
        self.assertTrue(plg_downloader.repository_type, "local_folder")

        # remote url
        plg_downloader = QgisPluginsDownloader(
            min_qgis_version="3.16",
            repository_source="//DSI/GIS/configurations/QGIS/3.16/plugins_production.xml",
        )
        self.assertTrue(plg_downloader.repository_type, "local_network")

        # remote url
        plg_downloader = QgisPluginsDownloader(
            min_qgis_version="3.16",
            repository_source="https://plugins.qgis.org/plugins/plugins.xml?qgis=3.16",
        )
        self.assertTrue(plg_downloader.repository_type, "remote_url")


# ############################################################################
# ####### Stand-alone run ########
# ################################
if __name__ == "__main__":
    unittest.main()
