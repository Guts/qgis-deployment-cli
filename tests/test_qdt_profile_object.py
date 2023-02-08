#! python3  # noqa E265

"""
    Usage from the repo root folder:

    .. code-block:: bash
        # for whole tests
        python -m unittest tests.test_qdt_profile_object
        # for specific test
        python -m unittest tests.test_qdt_profile_object.TestQdtProfile.test_profile_load_from_json_basic
"""

# standard
import unittest
from pathlib import Path

# project
from qgis_deployment_toolbelt.profiles.qdt_profile import QdtProfile

# ############################################################################
# ########## Classes #############
# ################################


class TestQdtProfile(unittest.TestCase):
    """Test QDT profile abstraction class."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        cls.good_profiles_files = sorted(
            Path("tests/fixtures/").glob("profiles/good_*.json")
        )

    def test_profile_load_from_json_basic(self):
        """Test profile loading from JSON."""
        for i in self.good_profiles_files:
            qdt_profile = QdtProfile.from_json(profile_json_path=i)
            self.assertIsInstance(qdt_profile, QdtProfile)

            # attributes types
            self.assertIsInstance(qdt_profile.name, str)
            self.assertIsInstance(qdt_profile.version, str)
            self.assertIsInstance(qdt_profile.plugins, list)

    def test_profile_load_from_json_with_parent_folder(self):
        """Test profile loading from JSON specifying parent folder."""
        for i in self.good_profiles_files:
            qdt_profile = QdtProfile.from_json(i, i.parent)
            self.assertIsInstance(qdt_profile, QdtProfile)

            # attributes types
            self.assertIsInstance(qdt_profile.name, str)
            self.assertIsInstance(qdt_profile.version, str)
            self.assertIsInstance(qdt_profile.plugins, list)

    def test_profile_load_from_json_complete(self):
        """Test profile loading from JSON."""
        for i in filter(lambda x: "complete" in x.name, self.good_profiles_files):
            qdt_profile = QdtProfile.from_json(i, i.parent)
            self.assertIsInstance(qdt_profile, QdtProfile)

            # attributes types
            self.assertIsInstance(qdt_profile.name, str)
            self.assertIsInstance(qdt_profile.alias, str)
            self.assertIsInstance(qdt_profile.folder, Path)
            self.assertIsInstance(qdt_profile.splash, (str, Path))
            self.assertIsInstance(qdt_profile.version, str)

            # attributes values
            self.assertEqual(i.parent.resolve(), qdt_profile.folder)


# ############################################################################
# ####### Stand-alone run ########
# ################################
if __name__ == "__main__":
    unittest.main()
