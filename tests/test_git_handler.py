#! python3  # noqa E265

"""Usage from the repo root folder:

    .. code-block:: python

        # for whole test
        python -m unittest tests.test_git_handler
        # for specific
        python -m unittest tests.test_git_handler.TestGitHandler.test_git_url_parsed
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import tempfile
import unittest
from pathlib import Path
from shutil import rmtree
from sys import version_info

# 3rd party
from giturlparse import GitUrlParsed

# package
from qgis_deployment_toolbelt.profiles.remote_git_handler import RemoteGitHandler

# #############################################################################
# ########## Classes ###############
# ##################################


class TestGitHandler(unittest.TestCase):
    """Test module."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        cls.good_git_url = "https://gitlab.com/Oslandia/qgis/profils_qgis_fr_2022.git"

    # standard methods
    def setUp(self):
        """Fixtures prepared before each test."""
        pass

    def tearDown(self):
        """Executed after each test."""
        pass

    # -- TESTS ---------------------------------------------------------
    def test_initialization(self):
        """Test remote git repo identifier"""
        # OK
        self.good_git_url = "https://gitlab.com/Oslandia/qgis/profils_qgis_fr_2022.git"
        self.assertTrue(RemoteGitHandler(self.good_git_url).is_url_git_repository)

        # KO
        bad_git_url = "https://oslandia.com"
        with self.assertRaises(ValueError):
            RemoteGitHandler(bad_git_url)

    def test_is_local_git_repo(self):
        """Test local git repo identifier"""
        self.good_git_url = "https://gitlab.com/Oslandia/qgis/profils_qgis_fr_2022.git"
        git_handler = RemoteGitHandler(self.good_git_url)

        # OK
        self.assertTrue(git_handler.is_local_path_git_repository(Path(".")))
        # KO
        self.assertFalse(git_handler.is_local_path_git_repository(Path("./tests")))

    def test_git_url_parsed(self):
        """Test git parsed URL"""
        self.good_git_url = "https://gitlab.com/Oslandia/qgis/profils_qgis_fr_2022.git"
        git_handler = RemoteGitHandler(self.good_git_url)

        # type
        self.assertIsInstance(git_handler.url_parsed, GitUrlParsed)

        # keys
        self.assertIn("branch", git_handler.url_parsed.data)
        self.assertIn("domain", git_handler.url_parsed.data)
        self.assertIn("groups_path", git_handler.url_parsed.data)
        self.assertIn("owner", git_handler.url_parsed.data)
        self.assertIn("path", git_handler.url_parsed.data)
        self.assertIn("path_raw", git_handler.url_parsed.data)
        self.assertIn("pathname", git_handler.url_parsed.data)
        self.assertIn("platform", git_handler.url_parsed.data)
        self.assertIn("port", git_handler.url_parsed.data)
        self.assertIn("protocol", git_handler.url_parsed.data)
        self.assertIn("protocols", git_handler.url_parsed.data)
        self.assertIn("repo", git_handler.url_parsed.data)
        self.assertIn("url", git_handler.url_parsed.data)

        # values
        self.assertIn("gitlab.com", git_handler.url_parsed.domain)
        self.assertIn("gitlab.com", git_handler.url_parsed.host)
        self.assertEqual("qgis", git_handler.url_parsed.groups_path)
        self.assertEqual("Oslandia", git_handler.url_parsed.owner)
        self.assertEqual("gitlab", git_handler.url_parsed.platform)
        self.assertEqual("profils_qgis_fr_2022", git_handler.url_parsed.repo)

    @unittest.skipUnless(version_info.minor >= 10, "requires python 3.10")
    def test_git_clone_py310(self):
        """Test git parsed URL.

        TODO: remove the decorator when python 3.8 and 3.9 are not supported anymore"""
        self.good_git_url = "https://gitlab.com/Oslandia/qgis/profils_qgis_fr_2022.git"
        git_handler = RemoteGitHandler(self.good_git_url)

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdirname:
            local_dest = Path(tmpdirname) / "test_git_clone"
            # clone
            git_handler.download(local_path=local_dest)
            # check if clone worked and new folder is a local git repo
            self.assertTrue(git_handler.is_local_path_git_repository(local_dest))

            # check pull is working
            git_handler.clone_or_pull(local_path=local_dest)

    def test_git_clone_py38(self):
        """Test git parsed URL.

        TODO: remove this test when python 3.8 and 3.9 are not supported anymore"""
        self.good_git_url = "https://gitlab.com/Oslandia/qgis/profils_qgis_fr_2022.git"
        git_handler = RemoteGitHandler(self.good_git_url)

        # test folder
        local_dest = Path(".") / "tests/fixtures/test_git_clone"

        # clone
        git_handler.download(local_path=local_dest.resolve())
        # check if clone worked and new folder is a local git repo
        self.assertTrue(git_handler.is_local_path_git_repository(local_dest))

        # check pull is working
        git_handler.clone_or_pull(local_path=local_dest)

        rmtree(local_dest, ignore_errors=True)
