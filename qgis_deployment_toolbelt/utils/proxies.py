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
from os import environ
from timeit import default_timer
from urllib.request import getproxies

# #############################################################################
# ########## Globals ###############
# ##################################

# chronometer
START_TIME = default_timer()

# logs
logger = logging.getLogger(__name__)

# default CLI context.
# See: https://click.palletsprojects.com/en/7.x/commands/#context-defaults
CONTEXT_SETTINGS = dict(obj={})

# #############################################################################
# ########## Functions #############
# ##################################


def proxy_settings():
    """Retrieves network proxy settings from OS or an environment file."""
    if environ.get("HTTP_PROXY") or environ.get("HTTPS_PROXY"):
        proxy_settings = {
            "http": environ.get("HTTP_PROXY"),
            "https": environ.get("HTTPS_PROXY"),
        }
        logger.debug(
            "Proxies settings found in environment vars (loaded from .env file): {}".format(
                proxy_settings
            )
        )
    elif getproxies():
        proxy_settings = getproxies()
        logger.debug("Proxies settings found in the OS: {}".format(proxy_settings))
    else:
        logger.debug("No proxy settings found in environment vars nor OS settings.")
        proxy_settings = None

    return proxy_settings


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
