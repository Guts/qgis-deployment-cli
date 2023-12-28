#! python3  # noqa: E265

"""
    Small module to get network proxies configuration.

    Author: Julien Moura (github.com/guts)
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from functools import lru_cache
from os import environ
from urllib.request import getproxies

# package
from qgis_deployment_toolbelt.utils.url_helpers import check_str_is_url

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Functions #############
# ##################################
@lru_cache
def get_proxy_settings() -> dict:
    """Retrieves network proxy settings from operating system configuration or
    environment variables.

    Returns:
        dict: proxy settings with protocl as key and URL as value
    """
    proxy_settings = {}
    if environ.get("QDT_PROXY_HTTP"):
        proxy_settings = {
            "http": environ.get("QDT_PROXY_HTTP"),
            "https": environ.get("QDT_PROXY_HTTP"),
        }
        logger.info(
            "Proxies settings from custom QDT in environment vars (QDT_PROXY_HTTP): "
            f"{proxy_settings}"
        )
    elif environ.get("HTTP_PROXY") or environ.get("HTTPS_PROXY"):
        if environ.get("HTTP_PROXY") and environ.get("HTTPS_PROXY"):
            proxy_settings = {
                "http": environ.get("HTTP_PROXY"),
                "https": environ.get("HTTPS_PROXY"),
            }
            logger.info(
                "Proxies settings from generic environment vars (HTTP_PROXY "
                f"and HTTPS_PROXY): {proxy_settings}"
            )
        elif environ.get("HTTP_PROXY") and not environ.get("HTTPS_PROXY"):
            proxy_settings = {
                "http": environ.get("HTTP_PROXY"),
            }
            logger.info(
                "Proxies settings from generic environment vars (HTTP_PROXY only): "
                f"{proxy_settings}"
            )
        elif not environ.get("HTTP_PROXY") and environ.get("HTTPS_PROXY"):
            proxy_settings = {
                "https": environ.get("HTTPS_PROXY"),
            }
            logger.info(
                "Proxies settings from generic environment vars (HTTPS_PROXY only): "
                f"{proxy_settings}"
            )
    elif getproxies():
        proxy_settings = getproxies()
        logger.debug(f"Proxies settings found in the OS: {proxy_settings}")
    else:
        logger.debug("No proxy settings found in environment vars nor OS settings.")

    # check scheme and URL validity
    if isinstance(proxy_settings, dict):
        for scheme, proxy_url in proxy_settings.items():
            if not check_str_is_url(input_str=proxy_url, raise_error=False):
                logger.warning(
                    f"Proxy value for {scheme} is not a valid URL: {proxy_url}. Can "
                    "lead to troubles."
                )

    return proxy_settings


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
