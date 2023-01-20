#! python3  # noqa: E265


# ############################################################################
# ########## IMPORTS #############
# ################################

# standard library
import logging
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import (
    ProxyHandler,
    Request,
    build_opener,
    getproxies,
    install_opener,
    urlopen,
)

# package
from qgis_deployment_toolbelt.__about__ import __title_clean__, __version__

# ############################################################################
# ########## GLOBALS #############
# ################################

# logs
logger = logging.getLogger(__name__)

# Handle network proxy
proxies_settings = getproxies()  # Get the system proxy settings
proxy_handler = ProxyHandler(proxies_settings)  # Create a proxy handler
opener = build_opener(proxy_handler)  # Create an opener that will use the proxy
install_opener(opener)  # Install the opener

# ############################################################################
# ########## FUNCTIONS ###########
# ################################


def download_remote_file_to_local(
    remote_url_to_download: str,
    local_file_path: Path,
    user_agent: str = f"{__title_clean__}/{__version__}",
    content_type: str = None,
    chunk_size: int = 8192,
) -> Path:
    """Check if the local index file exists. If not, download the search index from \
        remote URL. If it does exist, check if it has been modified.

    Args:
        remote_url_to_download (str): remote URL of the search index
        local_file_path (Path): local path to the index file
        user_agent (str, optional): user agent to use to perform the request. Defaults \
            to f"{__title_clean__}/{__version__}".
        content_type (str): HTTP content-type.
        chunk_size (int): size of each chunk to read and write in bytes.

    Returns:
        Path: path to the local file (should be the same as local_file_path)
    """
    # check if file exists
    if local_file_path.exists():
        logger.warning(f"{local_file_path} already exists. It's about to be replaced.")
        local_file_path.unlink(missing_ok=True)

    # mkae sure parents folder exist
    local_file_path.parent.mkdir(parents=True, exist_ok=True)

    # headers
    headers = {"User-Agent": user_agent}
    if content_type:
        headers["Accept"] = content_type

    # download the remote file into local file
    custom_request = Request(url=remote_url_to_download, headers=headers)

    try:
        with urlopen(custom_request) as response, local_file_path.open(
            mode="wb"
        ) as buffile:
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                buffile.write(chunk)
        logger.info(
            f"Downloading {remote_url_to_download} to {local_file_path} succeeded."
        )
    except HTTPError as error:
        logger.error(
            f"Downloading {remote_url_to_download} to {local_file_path} failed. "
            f"Cause: HTTPError. Trace: {error}"
        )
        raise error
    except URLError as error:
        logger.error(
            f"Downloading {remote_url_to_download} to {local_file_path} failed. "
            f"Cause: URLError. Trace: {error}"
        )
        raise error
    except TimeoutError as error:
        logger.error(
            f"Downloading {remote_url_to_download} to {local_file_path} failed. "
            f"Cause: TimeoutError. Trace: {error}"
        )
        raise error
    except Exception as error:
        logger.error(
            f"Downloading {remote_url_to_download} to {local_file_path} failed. "
            f"Cause: Unknown error. Trace: {error}"
        )
        raise error

    return local_file_path
