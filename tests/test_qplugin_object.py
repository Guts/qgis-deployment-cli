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

    def test_qplugin_load_from_dict(self):
        """Test profile loading from JSON."""
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


# ############################################################################
# ####### Stand-alone run ########
# ################################
if __name__ == "__main__":
    unittest.main()
