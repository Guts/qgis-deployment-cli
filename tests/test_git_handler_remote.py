#! python3  # noqa E265

"""Usage from the repo root folder:

    .. code-block:: python

        # for whole test
        python -m unittest tests.test_git_handler_remote
        # for specific
        python -m unittest tests.test_git_handler_remote.TestGitHandlerRemote.test_git_url_parsed
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import tempfile
import unittest
from pathlib import Path

# 3rd party
from dulwich.errors import NotGitRepository
from giturlparse import GitUrlParsed

# package
from qgis_deployment_toolbelt.profiles.remote_git_handler import RemoteGitHandler

# #############################################################################
# ########## Classes ###############
# ##################################


class TestGitHandlerRemote(unittest.TestCase):
    """Test module."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        cls.good_git_url = "https://gitlab.com/Oslandia/qgis/profils_qgis_fr_2022.git"

    # -- TESTS ---------------------------------------------------------
    def test_initialization(self):
        """Test remote git repo identifier"""
        # OK
        self.good_git_url = "https://gitlab.com/Oslandia/qgis/profils_qgis_fr_2022.git"
        remote_git_handler = RemoteGitHandler(self.good_git_url)

        self.assertEqual(remote_git_handler.SOURCE_REPOSITORY_TYPE, "git_remote")
        self.assertTrue(remote_git_handler.is_valid_git_repository())

        # KO
        bad_git_url = "https://oslandia.com"
        with self.assertRaises(NotGitRepository):
            RemoteGitHandler(bad_git_url)

    def test_is_local_git_repo(self):
        """Test local git repo identifier"""
        self.good_git_url = "https://gitlab.com/Oslandia/qgis/profils_qgis_fr_2022.git"
        git_handler = RemoteGitHandler(self.good_git_url)

        # OK
        self.assertTrue(git_handler._is_local_path_git_repository(Path(".")))
        # KO
        self.assertFalse(git_handler._is_local_path_git_repository(Path("./tests")))

    def test_git_url_parsed(self):
        """Test git parsed URL"""
        self.good_git_url = "https://gitlab.com/Oslandia/qgis/profils_qgis_fr_2022.git"
        git_handler = RemoteGitHandler(self.good_git_url)
        git_url_parsed = git_handler.url_parsed(self.good_git_url)

        # type
        self.assertIsInstance(git_url_parsed, GitUrlParsed)

        # keys
        self.assertIn("branch", git_url_parsed.data)
        self.assertIn("domain", git_url_parsed.data)
        self.assertIn("groups_path", git_url_parsed.data)
        self.assertIn("owner", git_url_parsed.data)
        self.assertIn("path", git_url_parsed.data)
        self.assertIn("path_raw", git_url_parsed.data)
        self.assertIn("pathname", git_url_parsed.data)
        self.assertIn("platform", git_url_parsed.data)
        self.assertIn("port", git_url_parsed.data)
        self.assertIn("protocol", git_url_parsed.data)
        self.assertIn("protocols", git_url_parsed.data)
        self.assertIn("repo", git_url_parsed.data)
        self.assertIn("url", git_url_parsed.data)

        # values
        self.assertIn("gitlab.com", git_url_parsed.domain)
        self.assertIn("gitlab.com", git_url_parsed.host)
        self.assertEqual("qgis", git_url_parsed.groups_path)
        self.assertEqual("Oslandia", git_url_parsed.owner)
        self.assertEqual("gitlab", git_url_parsed.platform)
        self.assertEqual("profils_qgis_fr_2022", git_url_parsed.repo)

    def test_git_clone_remote_url(self):
        """Test git parsed URL."""
        self.good_git_url = "https://gitlab.com/Oslandia/qgis/profils_qgis_fr_2022.git"
        git_handler = RemoteGitHandler(self.good_git_url)

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdirname:
            local_dest = Path(tmpdirname) / "test_git_clone"
            # clone
            git_handler.download(destination_local_path=local_dest)
            # check if clone worked and new folder is a local git repo
            self.assertTrue(git_handler._is_local_path_git_repository(local_dest))

            # check pull is working
            git_handler.clone_or_pull(to_local_destination_path=local_dest)
