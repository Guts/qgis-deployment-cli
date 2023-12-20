#! python3  # noqa: E265

"""
    Minimalist client HTTP but only based on pure standard lib

    Author: Julien Moura (https://github.com/guts)
"""

# ############################################################################
# ########## IMPORTS #############
# ################################

# standard library
import http.client
import json
import logging
import socket
import ssl
import urllib.parse
from base64 import b64encode
from contextlib import contextmanager
from http.client import HTTPResponse
from pathlib import Path
from typing import Any, Literal

# package
from qgis_deployment_toolbelt.__about__ import __title_clean__, __version__
from qgis_deployment_toolbelt.utils.formatters import convert_octets
from qgis_deployment_toolbelt.utils.proxies import get_proxy_settings

# ############################################################################
# ########## GLOBALS #############
# ################################

# logs
logger = logging.getLogger(__name__)


# ############################################################################
# ########## CLASSES #############
# ################################


class EnhancedHTTPResponse(HTTPResponse):
    """An enhanced HTTP Response object with some helping attributes."""

    def __init__(self, http_response: HTTPResponse | None = None):
        """Instanciation method.

        Args:
            http_response (HTTPResponse | None, optional): parent class to extend.
                Defaults to None.
        """
        self._response = http_response
        # content to fake the behavior of requests package
        self.content: bytes = b""
        self.content_json: dict | None = None

    @property
    def is_content_json(self) -> bool:
        """Check if the content is a valid JSON object. If so, the content is loaded
        into the self.content_json attribute.

        Returns:
            bool: True is the content is a valid JSON. False if not.
        """
        if isinstance(self.content, (str, bytes, bytearray)) and len(self.content):
            try:
                self.content_json = json.loads(self.content)
                logger.debug(
                    "Response content is a valid JSON and has been deserialized into "
                    "'content_json' attribute."
                )
            except ValueError as err:
                logger.debug(f"Response content is not a valid JSON. Trace: {err}")
                return False
            return True
        else:
            logger.debug(
                "Response content is empty or not a valid type (str, bytes, bytearray): "
                f"{type(self.content), len(self.content)}"
            )
            return False

    def __getattr__(self, attr: Any):
        """Redirect calls to embedded HTTPResponse attribute.

        Args:
            attr (Any): attribute

        Returns:
            Any: attribute value
        """
        return getattr(self._response, attr)


class SimpleHttpClient:
    """Simple HTTP client class that supports GET, POST, PUT, HEAD, OPTIONS, DELETE
        requests, file downloads and some authentication flow, using only standard
        Python modules (mainly http.client).

    Example:
        .. code-block:: python

            client = SimpleHttpClient(
                    default_headers={"Content-Type": "application/json"}
                    )
            response = client.get("http://api.example.com/entity")
            print(response.status, response.reason)
            # 200, 'OK'
            print(response.content) # body as bytes
            # b'{"user"...}'
            local_path = client.download_file("http://example.com/somefile.txt", Path("localfile.txt"))
    """

    def __init__(
        self,
        default_headers: dict[str, str]
        | None = {
            "User-Agent": f"{__title_clean__}/{__version__}",
        },
        timeout: int | None = 30,
        ssl_disable_check: bool = False,
    ):
        """
        Initialize the SimpleHttpClient.

        Args:
            default_headers (dict[str,str] | None, optional): Default headers to include
                in all requests. Defaults to
                { "User-Agent": f"{__title_clean__}/{__version__}", }.
            timeout (int | None, optional): _description_. Defaults to 30.
        """
        self.auth = None
        self.default_headers = default_headers
        self.ssl_check_disabled = ssl_disable_check
        self.timeout = timeout
        self.proxy_settings = get_proxy_settings()

        # prepare SSL context depending on options
        if self.ssl_check_disabled:
            self.ssl_context = ssl._create_unverified_context()
        else:
            self.ssl_context = None
        # if defined, set timeout to socket module
        if self.timeout is not None:
            socket.setdefaulttimeout(self.timeout)

    def _parse_url(self, url: str) -> tuple[str, str, int, str]:
        """
        Parse the URL and extract scheme, host, port and path.

        Args:
            url: The URL to parse.

        Returns:
            A tuple containing scheme, host, port and path.
        """
        parsed_url = urllib.parse.urlparse(url)
        scheme = parsed_url.scheme
        host = parsed_url.netloc
        port = parsed_url.port or (443 if scheme == "https" else 80)  # default port
        path = parsed_url.path

        return scheme, host, port, path

    @contextmanager
    def _send_request(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        body: str | None = None,
        load_content: bool = True,
    ) -> EnhancedHTTPResponse:
        """Send an HTTP request.

        Args:
            method (str): The HTTP method to use (e.g., "GET", "POST", "PUT", "HEAD",
                "OPTIONS", "DELETE").
            url (str): The URL to send the request to.
            headers (dict[str, str] | None, optional): Additional headers to include in
                the request.
            body (str | None, optional): The request body for methods like POST and PUT.
            load_content (bool, optional): option to load content in the content
                attribute. Defaults to True.

        Returns:
            EnhancedHTTPResponse: The HTTPResponse object.

        Yields:
            Iterator[EnhancedHTTPResponse]: The HTTPResponse object.
        """
        # Combine default_headers and headers
        combined_headers = {**self.default_headers, **(headers or {})}

        # Ajouter l'authentification aux headers si elle est définie
        if self.auth:
            headers["Authorization"] = self.auth

        # parse URL
        scheme, host, port, path = self._parse_url(url)

        # handle different HTTP schemes
        if scheme == "https":
            if isinstance(self.proxy_settings, dict) and "https" in self.proxy_settings:
                conn = http.client.HTTPSConnection(
                    self.proxy_settings.get("https"),
                    timeout=self.timeout,
                    context=self.ssl_context,
                )
                conn.set_tunnel(host=host, port=port, headers=combined_headers)
            else:
                conn = http.client.HTTPSConnection(
                    host=host, port=port, timeout=self.timeout
                )
        else:
            if isinstance(self.proxy_settings, dict) and "http" in self.proxy_settings:
                conn = http.client.HTTPConnection(
                    self.proxy_settings.get("http"), port=port, timeout=self.timeout
                )
                conn.set_tunnel(host=host, port=port, headers=combined_headers)
            else:
                conn = http.client.HTTPConnection(
                    host=host, port=port, timeout=self.timeout
                )

        # prepare response_body
        response = EnhancedHTTPResponse()
        response_body = None

        # make request
        try:
            is_redirected: bool = True
            while is_redirected:
                conn.request(
                    method=method, url=path, body=body, headers=combined_headers
                )
                response = EnhancedHTTPResponse(conn.getresponse())

                # handle redirections
                if response.status // 100 == 3 and "Location" in response.headers:
                    # Handle redirection
                    location = response.headers["Location"]
                    response.close()  # Close the previous response

                    # Retry the request with the new URL and the same headers
                    conn.request(method, location, body=body, headers=combined_headers)
                    response = conn.getresponse()
                elif response.status // 100 == 3 and "Location" not in response.headers:
                    logger.error(
                        f"Request {method.upper()} to {url} received a redirection code "
                        f"{response.status} but no new location."
                    )
                    is_redirected = False
                else:
                    # Exit the loop if no redirection
                    is_redirected = False

            logger.info(
                f"La requête {method} vers {url} a fonctionné. "
                f"Headers de la requête = {combined_headers} | {body=}"
            )

            # if option is enabled, load full content
            if load_content:
                response_body = response.read()
            else:
                response_body = None

            yield response

        except http.client.HTTPException as err:
            logger.error(f"HTTP Exception occurred: {err}")
            raise err

        except TimeoutError as err:
            logger.error(f"Request timed out. timeout set: {self.timeout}")
            raise err

        except Exception as err:
            logger.error(f"An unexpected error occurred: {err}")
            raise err

        finally:
            # conn.close()
            response.content = response_body

    def auth_set_basic(self, username: str, password: str) -> None:
        """
        Set the Basic Authentication credentials.

        Args:
            username: The username for Basic Authentication.
            password: The password for Basic Authentication.

        Example:
            .. code-block:: python

                client = SimpleHttpClient()
                client.auth_set_basic("myusername", "mypassword")
                response = client.get("http://example.com")
        """
        auth_str = f"{username}:{password}"
        auth_bytes = auth_str.encode("utf-8")
        self.auth = "Basic " + b64encode(auth_bytes).decode("utf-8")

    def auth_set_bearer_token(self, token: str) -> None:
        """Set the Bearer token for authentication.

        Args:
            token: The Bearer token.

        Example:
            .. code-block:: python

                client = SimpleHttpClient()
                client.auth_set_bearer_token("my_access_token")
                response = client.get("http://example.com")
        """
        self.auth = "Bearer " + token

    def delete(
        self, url: str, headers: dict[str, str] | None = None
    ) -> EnhancedHTTPResponse:
        """Send a DELETE request.

        Args:
            url: The URL to send the request to.
            headers: Additional headers to include in the request.

        Returns:
            The HTTPResponse object.
        """
        with self._send_request("DELETE", url, headers=headers) as response:
            return response

    def download_file(
        self,
        url: str,
        destination: str | Path,
        method: Literal["GET", "POST"] = "GET",
        chunk_size: int = 8192,
        data: dict | None = None,
        headers: dict[str, str] | None = None,
    ) -> Path | HTTPResponse:
        """Download a file from the given URL and save it to the specified destination.

        Args:
            url (str): The URL of the file to download.
            destination (str|Path): The local path where the downloaded file will be saved.
            chunk_size (int, optional): The size of each download chunk in bytes. Defaults to 8192.
            headers: Additional headers to include in the request.

        Returns:
            Path | HTTPResponse: destination path if download succeeded.
            HTTPResponse if it failed.
        """
        destination = Path(destination)

        # make sure parents folder exist
        destination.parent.mkdir(parents=True, exist_ok=True)

        # handle HTTP method and args
        if method.lower() == "post" or data is not None:
            if data:
                body = urllib.parse.urlencode(data)
                headers = headers or {}
                headers["Content-type"] = "application/x-www-form-urlencoded"
            request_args = {
                "method": "POST",
                "url": url,
                "headers": headers,
                "body": body,
                "load_content": False,
            }
        else:
            request_args = {
                "method": "GET",
                "url": url,
                "headers": headers,
                "load_content": False,
            }

        # perform request
        with destination.open(mode="wb") as buffile, self._send_request(
            **request_args
        ) as response:
            if response.status == 200:
                # Download the file in chunks and save to disk
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    buffile.write(chunk)
            else:
                logger.error(
                    f"Failed to download file from {url} to {destination}. "
                    f"Status Code: {response.status}"
                )
                return response

        logger.info(
            f"Le téléchargement du fichier distant {url} dans "
            f"{destination} ({convert_octets(destination.stat().st_size)}) a réussi."
        )
        return destination

    def get(
        self, url: str, headers: dict[str, str] | None = None
    ) -> EnhancedHTTPResponse:
        """
        Send a GET request.

        Args:
            url: The URL to send the request to.
            headers: Additional headers to include in the request.

        Returns:
            The HTTPResponse object.

        Example:
            .. code-block:: python

                client = SimpleHttpClient()
                response = client.get("http://example.com")
                print(response.status, response.reason)
                print(response.content)
        """
        with self._send_request("GET", url, headers=headers) as response:
            return response

    def head(
        self, url: str, headers: dict[str, str] | None = None
    ) -> EnhancedHTTPResponse:
        """
        Send a HEAD request.

        Args:
            url: The URL to send the request to.
            headers: Additional headers to include in the request.

        Returns:
            The HTTPResponse object.
        """
        with self._send_request("HEAD", url, headers=headers) as response:
            return response

    def options(
        self, url: str, headers: dict[str, str] | None = None
    ) -> EnhancedHTTPResponse:
        """
        Send an OPTIONS request.

        Args:
            url: The URL to send the request to.
            headers: Additional headers to include in the request.

        Returns:
            The HTTPResponse object.
        """
        with self._send_request("OPTIONS", url, headers=headers) as response:
            return response

    def post(
        self,
        url: str,
        data: dict[str, str | int] | None = None,
        headers: dict[str, str] | None = None,
    ) -> EnhancedHTTPResponse:
        """
        Send a POST request.

        Args:
            url: The URL to send the request to.
            data: The data to include in the request body.
            headers: Additional headers to include in the request.

        Returns:
            The HTTPResponse object.
        """
        body = None
        if data:
            body = urllib.parse.urlencode(data)
            headers = headers or {}
            headers["Content-type"] = "application/x-www-form-urlencoded"

        with self._send_request("POST", url, headers=headers, body=body) as response:
            return response

    def put(
        self,
        url: str,
        data: dict[str, str | int] | None = None,
        headers: dict[str, str] | None = None,
    ) -> EnhancedHTTPResponse:
        """
        Send a PUT request.

        Args:
            url: The URL to send the request to.
            data: The data to include in the request body.
            headers: Additional headers to include in the request.

        Returns:
            The HTTPResponse object.
        """
        body = None
        if data:
            body = urllib.parse.urlencode(data)
            headers = headers or {}
            headers["Content-type"] = "application/x-www-form-urlencoded"

        with self._send_request("PUT", url, headers=headers, body=body) as response:
            return response


if __name__ == "__main__":
    """Stand-alone execution"""
    logging.basicConfig(level=logging.DEBUG)
    pass

    client = SimpleHttpClient(timeout=60)

    # response = client.get("http://localhost:9753/get")
    # print(
    #     f"{response.status=},\n{response.reason=},\n{response.headers=},\n{response.isclosed()=}\n{response.content=}"
    # )

    # print("\n\twith requests")

    import json
    import pprint

    # r = requests.get("http://localhost:9753/get")
    # print(response.content)
    # print(r.content)

    token_path = client.download_file(
        url="https://panoramax.ign.fr/api/auth/tokens/generate",
        headers={"accept": "application/json"},
        data={"description": "GPF Toolbelt"},
        destination=Path("/tmp/ign/panoramax/token.json"),
    )
    print(type(token_path), token_path)
    token_claim_url = json.loads(token_path.read_bytes())
    pprint.pprint(token_claim_url)

    client = SimpleHttpClient()
    file_path = client.download_file(
        url="https://speed.hetzner.de/100MB.bin",
        destination=Path("/tmp/ign/toolbelt/plop.bin"),
    )
    print(file_path.exists())
