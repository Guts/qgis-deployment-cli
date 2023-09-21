#! python3  # noqa E265

"""
    Usage from the repo root folder:

    .. code-block:: bash
        # for whole tests
        python -m unittest tests.test_utils_simple_http_client
        # for specific test
        python -m unittest tests.test_utils_simple_http_client.TestSimpleHttpClient.test_download_file
"""

# standard
import unittest
from os import environ

# 3rd party
import pytest_httpbin

from qgis_deployment_toolbelt.utils.proxies import get_proxy_settings

# package
from qgis_deployment_toolbelt.utils.simple_http_client import (
    EnhancedHTTPResponse,
    SimpleHttpClient,
)


@pytest_httpbin.use_class_based_httpbin
@pytest_httpbin.use_class_based_httpbin_secure
class TestSimpleHttpClientHttpbin(unittest.TestCase):
    def test_http(self):
        get_proxy_settings.cache_clear()
        client = SimpleHttpClient()
        resp = client.get(self.httpbin.url + "/get")
        assert isinstance(resp, EnhancedHTTPResponse)
        assert resp.status == 200, self.httpbin.url

    def test_http_secure(self):
        environ["SSL_CERT_FILE"] = pytest_httpbin.certs.where()
        client = SimpleHttpClient(ssl_disable_check=True)
        resp = client.get(self.httpbin_secure.url + "/get")
        self.assertEqual(resp.status, 200, resp.content)


if __name__ == "__main__":
    unittest.main()
