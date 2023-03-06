#! python3  # noqa E265

"""
    Usage from the repo root folder:

    .. code-block:: bash
        # for whole tests
        python -m unittest tests.test_utils
        # for specific test
        python -m unittest tests.test_utils.TestUtils.test_slugger
"""

# standard library
import unittest
from os import environ
from sys import platform as opersys

# project
from qgis_deployment_toolbelt.utils import get_proxy_settings
from qgis_deployment_toolbelt.utils.win32utils import get_environment_variable

# ############################################################################
# ########## Classes #############
# ################################


class TestUtils(unittest.TestCase):
    """Test package utilities."""

    def test_proxy_settings(self):
        """Test proxy settings retriever."""
        # OK
        self.assertIsNone(get_proxy_settings())
        environ["HTTP_PROXY"] = "http://proxy.example.com:3128"
        self.assertIsInstance(get_proxy_settings(), dict)

    @unittest.skipIf(opersys != "win32", "Test specific to Windows.")
    def test_win32_getenv(self):
        """Test specific Windows environment variable getter."""
        # OK
        self.assertIsInstance(get_environment_variable("TEMP"), str)

        # KO
        self.assertIsNone(get_environment_variable("YOUPI"))


# ############################################################################
# ####### Stand-alone run ########
# ################################
if __name__ == "__main__":
    unittest.main()
