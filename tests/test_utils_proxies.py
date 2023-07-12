#! python3  # noqa E265

"""
    Usage from the repo root folder:

    .. code-block:: bash
        # for whole tests
        python -m unittest tests.test_utils_proxies
        # for specific test
        python -m unittest tests.test_utils_proxies.TestUtilsNetworkProxies.test_proxy_settings
"""

# standard library
import unittest
from os import environ

# project
from qgis_deployment_toolbelt.utils import get_proxy_settings

# ############################################################################
# ########## Classes #############
# ################################


class TestUtilsNetworkProxies(unittest.TestCase):
    """Test network proxy utilities."""

    def test_proxy_settings(self):
        """Test proxy settings retriever."""
        # by default, no proxy
        self.assertIsNone(get_proxy_settings())

        # using generic - only http
        environ["HTTP_PROXY"] = "http://proxy.example.com:3128"
        self.assertIsInstance(get_proxy_settings(), dict)
        self.assertEqual(
            get_proxy_settings().get("http"), "http://proxy.example.com:3128"
        )
        self.assertIsNone(get_proxy_settings().get("https"))

        environ.pop("HTTP_PROXY")  # clean up

        # using generic - only https
        environ["HTTPS_PROXY"] = "https://proxy.example.com:3128"
        self.assertIsInstance(get_proxy_settings(), dict)
        self.assertEqual(
            get_proxy_settings().get("https"), "https://proxy.example.com:3128"
        )
        self.assertIsNone(get_proxy_settings().get("http"))

        environ.pop("HTTPS_PROXY")  # clean up

        # using generic - both http and https
        environ["HTTP_PROXY"] = "http://proxy.example.com:3128"
        environ["HTTPS_PROXY"] = "https://proxy.example.com:3128"
        self.assertIsInstance(get_proxy_settings(), dict)
        self.assertEqual(
            get_proxy_settings().get("https"), "https://proxy.example.com:3128"
        )
        self.assertEqual(
            get_proxy_settings().get("http"), "http://proxy.example.com:3128"
        )

        environ.pop("HTTP_PROXY")  # clean up
        environ.pop("HTTPS_PROXY")  # clean up

        # using custom QDT
        environ["QDT_PROXY_HTTP"] = "http://user:p8ùX45@proxy.example.com:3128"
        self.assertIsInstance(get_proxy_settings(), dict)
        self.assertEqual(
            get_proxy_settings().get("http"),
            "http://user:p8ùX45@proxy.example.com:3128",
        )
        self.assertEqual(
            get_proxy_settings().get("https"),
            "http://user:p8ùX45@proxy.example.com:3128",
        )

        environ.pop("QDT_PROXY_HTTP")  # clean up


# ############################################################################
# ####### Stand-alone run ########
# ################################
if __name__ == "__main__":
    unittest.main()
