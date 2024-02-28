#! python3  # noqa: E265


# ############################################################################
# ########## IMPORTS #############
# ################################

# standard library
import logging
from os import getenv
from pathlib import Path

# 3rd party
import truststore
from requests import Session
from requests.exceptions import ConnectionError, HTTPError
from requests.utils import requote_uri

# package
from qgis_deployment_toolbelt.__about__ import __title_clean__, __version__
from qgis_deployment_toolbelt.utils.formatters import convert_octets
from qgis_deployment_toolbelt.utils.proxies import get_proxy_settings
from qgis_deployment_toolbelt.utils.str2bool import str2bool

# ############################################################################
# ########## GLOBALS #############
# ################################

# logs
logger = logging.getLogger(__name__)

if str2bool(getenv("QDT_SSL_USE_SYSTEM_STORES", False)):
    truststore.inject_into_ssl()
    logger.debug("Option to use native system certificates stores is enabled.")

# ############################################################################
# ########## FUNCTIONS ###########
# ################################


def download_remote_file_to_local(
    remote_url_to_download: str,
    local_file_path: Path,
    user_agent: str = f"{__title_clean__}/{__version__}",
    content_type: str | None = None,
    chunk_size: int = 8192,
    timeout=(800, 800),
) -> Path:
    """Check if the local index file exists. If not, download the search index from \
        remote URL. If it does exist, check if it has been modified.

    Args:
        remote_url_to_download (str): remote URL of the search index
        local_file_path (Path): local path to the index file
        user_agent (str, optional): user agent to use to perform the request. Defaults \
            to f"{__title_clean__}/{__version__}".
        content_type (str | None, optional): HTTP content-type. Defaults to None.
        chunk_size (int, optional): size of each chunk to read and write in bytes. \
            Defaults to 8192.
        timeout (tuple, optional): custom timeout (request, response). Defaults to (800, 800).

    Returns:
        Path: path to the local file (should be the same as local_file_path)
    """
    # check if file exists
    if local_file_path.exists():
        logger.info(f"{local_file_path} already exists. It's about to be replaced.")
        local_file_path.unlink(missing_ok=True)

    # make sure parents folder exist
    local_file_path.parent.mkdir(parents=True, exist_ok=True)

    # headers
    headers = {"User-Agent": user_agent}
    if content_type:
        headers["Accept"] = content_type

    try:
        with Session() as dl_session:
            dl_session.proxies.update(get_proxy_settings())
            dl_session.headers.update(headers)

            with dl_session.get(
                url=requote_uri(remote_url_to_download), stream=True, timeout=timeout
            ) as req:
                req.raise_for_status()

                with local_file_path.open(mode="wb") as buffile:
                    for chunk in req.iter_content(chunk_size=chunk_size):
                        if chunk:
                            buffile.write(chunk)
            logger.info(
                f"Downloading {remote_url_to_download} to {local_file_path} "
                f"({convert_octets(local_file_path.stat().st_size)}) succeeded."
            )
    except HTTPError as error:
        logger.error(
            f"Downloading {remote_url_to_download} to {local_file_path} failed. "
            f"Cause: HTTPError. Trace: {error}"
        )
        raise error
    except ConnectionError as error:
        logger.error(
            f"Downloading {remote_url_to_download} to {local_file_path} failed. "
            f"Cause: ConnectionError. Trace: {error}"
        )
        raise error
    except Exception as error:
        logger.error(
            f"Downloading {remote_url_to_download} to {local_file_path} failed. "
            f"Cause: Unknown error. Trace: {error}"
        )
        raise error

    return local_file_path
