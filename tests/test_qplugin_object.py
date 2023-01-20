#! python3  # noqa E265

"""
    Usage from the repo root folder:

    .. code-block:: bash
        # for whole tests
        python -m unittest tests.test_qplugin_object
        # for specific test
        python -m unittest tests.test_qplugin_object.TestQgisPluginObject.test_profile_load_from_json_basic
"""

# standard
import unittest
from pathlib import Path

# project
from qgis_deployment_toolbelt.plugins.plugin import QgisPlugin
from qgis_deployment_toolbelt.profiles.qdt_profile import QdtProfile
from qgis_deployment_toolbelt.utils.file_downloader import download_remote_file_to_local

# ############################################################################
# ########## Classes #############
# ################################


class TestQgisPluginObject(unittest.TestCase):
    """Test QGIS Plugin abstraction class."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        cls.good_profiles_files = sorted(
            Path("tests/fixtures/").glob("profiles/good_*.json")
        )

    def test_qplugin_load_from_profile(self):
        """Test plugin object loading from profile object."""
        for p in self.good_profiles_files:
            qdt_profile = QdtProfile.from_json(
                profile_json_path=p,
                profile_folder=p.parent,
            )

            self.assertIsInstance(qdt_profile.plugins, list)
            if len(qdt_profile.plugins):
                for i in qdt_profile.plugins:
                    self.assertIsInstance(i, QgisPlugin)

    def test_qplugin_load_from_dict(self):
        """Test plugin object loading from JSON."""
        sample_plugin_complete = {
            "name": "french_locator_filter",
            "version": "1.0.4",
            "url": "https://plugins.qgis.org/plugins/french_locator_filter/version/1.0.4/download/",
            "type": "remote",
        }

        plugin_obj_one = QgisPlugin.from_dict(sample_plugin_complete)

        sample_plugin_incomplete = {
            "name": "french_locator_filter",
            "version": "1.0.4",
            "official_repository": True,
        }

        plugin_obj_two = QgisPlugin.from_dict(sample_plugin_incomplete)

        self.assertEqual(plugin_obj_one, plugin_obj_two)

    def test_qplugin_load_from_zip(self):
        """Test plugin object loading from a ZIP archive downloaded."""
        # plugin as dict
        sample_plugin_complex = {
            "name": "Layers menu from project",
            "version": "v2.0.6",
            "url": "https://plugins.qgis.org/plugins/menu_from_project/version/v2.0.6/download/",
            "type": "remote",
            "plugin_id": 1846,
        }
        # plugin as object
        plugin_obj: QgisPlugin = QgisPlugin.from_dict(sample_plugin_complex)

        # some attributes are not set
        self.assertIsNone(plugin_obj.folder_name)

        # prepare local download path
        local_plugin_download = Path(
            f"tests/fixtures/tmp/{plugin_obj.installation_folder_name}/"
            f"{plugin_obj.id_with_version}.zip"
        )

        # some attributes have been set
        self.assertIsNotNone(plugin_obj.folder_name)

        # download plugin zip archive
        download_remote_file_to_local(
            remote_url_to_download=plugin_obj.download_url,
            local_file_path=local_plugin_download.resolve(),
            content_type="application/zip",
        )

        # check download worked
        self.assertTrue(local_plugin_download.is_file())

        # load from zip
        plugin_obj_from_zip: QgisPlugin = QgisPlugin.from_zip(
            input_zip_path=local_plugin_download
        )

        # check types
        self.assertIsInstance(plugin_obj_from_zip.name, str)
        self.assertIsInstance(plugin_obj_from_zip.version, str)
        self.assertIsInstance(plugin_obj_from_zip.folder_name, str)
        self.assertIsInstance(plugin_obj_from_zip.qgis_maximum_version, str)
        self.assertIsInstance(plugin_obj_from_zip.qgis_minimum_version, str)

        # check values
        self.assertEqual(plugin_obj.name, plugin_obj_from_zip.name)
        self.assertEqual(plugin_obj.version, plugin_obj_from_zip.version)
        self.assertEqual(plugin_obj.folder_name, plugin_obj_from_zip.folder_name)


# ############################################################################
# ####### Stand-alone run ########
# ################################
if __name__ == "__main__":
    unittest.main()
