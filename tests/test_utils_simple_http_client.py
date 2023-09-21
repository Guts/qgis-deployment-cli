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
from pathlib import Path
from unittest.mock import MagicMock, patch

# package
from qgis_deployment_toolbelt.utils.simple_http_client import (
    EnhancedHTTPResponse,
    SimpleHttpClient,
)


class TestSimpleHttpClient(unittest.TestCase):
    def setUp(self):
        """Run before each test method."""
        self.client = SimpleHttpClient(timeout=5)

    def test_download_file(self):
        """Test file downloading."""
        dst_filepath = Path("./tests/fixtures/tmp/index.html")
        # Télécharger le fichier depuis le serveur HTTP local
        url = "https://duckduckgo.com/index.html"
        download_result = self.client.download_file(url, dst_filepath)

        self.assertIsInstance(download_result, Path)
        self.assertTrue(download_result.resolve(), dst_filepath.resolve())
        self.assertTrue(download_result.is_file())

        with dst_filepath.open("r") as fifi:
            lines = fifi.readlines()

        self.assertEqual(lines[0], "<!DOCTYPE html>\n")

        # clean up
        dst_filepath.unlink(missing_ok=True)

    def test_get(self):
        # Créer une réponse factice pour la méthode get
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.reason = "OK"
        mock_response.read.return_value = b"Response data"

        # Mocker la méthode get pour renvoyer la réponse factice
        with patch.object(SimpleHttpClient, "get", return_value=mock_response):
            # Effectuer la requête GET (en réalité, nous utilisons la réponse factice)
            response = self.client.get("http://fakeurl.intra/resource")

            # Vérifier les résultats
            self.assertEqual(response.status, 200)
            self.assertEqual(response.reason, "OK")
            self.assertEqual(response.read(), b"Response data")

    def test_post(self):
        # Créer une réponse factice pour la méthode post
        mock_response = MagicMock()
        mock_response.status = 201
        mock_response.reason = "Created"
        mock_response.read.return_value = b"Response data"

        # Mocker la méthode post pour renvoyer la réponse factice
        with patch.object(SimpleHttpClient, "post", return_value=mock_response):
            # Effectuer la requête POST (en réalité, nous utilisons la réponse factice)
            data = {"key": "value"}
            response = self.client.post("http://example.com/resource", data=data)

            # Vérifier les résultats
            self.assertEqual(response.status, 201)
            self.assertEqual(response.reason, "Created")
            self.assertEqual(response.read(), b"Response data")

    @patch("qgis_deployment_toolbelt.utils.proxies.get_proxy_settings")
    def test_get_request_with_proxy(self, mock_get_proxy_settings):
        # Mock the proxy settings
        mock_proxy_settings = {
            "http": "http://localhost:8080",
            "https": "http://localhost:8080",
        }
        mock_get_proxy_settings.return_value = mock_proxy_settings

        # Create an instance of your client with mock proxy settings
        client = SimpleHttpClient()

        # Mock the response from the proxy
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.reason = "OK"
        mock_response.read.return_value = b"Response Content"

        with patch("http.client.HTTPConnection") as mock_connection:
            mock_connection.return_value.getresponse.return_value = mock_response

            # Perform the test
            response = client.get("https://httpbin.org/get")

            # Assertions
            self.assertEqual(response.status, 200)
            self.assertIsInstance(response, EnhancedHTTPResponse)
            # self.assertEqual(response.content, b"Response Content")
            mock_connection.assert_called_with("localhost:8080", timeout=None)


if __name__ == "__main__":
    unittest.main()
