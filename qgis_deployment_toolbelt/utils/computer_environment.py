#! python3  # noqa: E265

"""
    Base of QDT jobs.

    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
import platform
from sys import platform as opersys

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Functions #############
# ##################################


def environment_dict() -> dict:
    """Returns a dictionary containing some environment information (computer, network,
        platform) that can be used in QDT various places: rules...

    Returns:
        dict: dict with some environment metadata to use in rules.
    """
    try:
        linux_distribution_name = f"{platform.freedesktop_os_release().get('NAME')}"
        linux_distribution_version = (
            f"{platform.freedesktop_os_release().get('VERSION_ID')}"
        )
    except OSError as err:
        logger.debug(f"Trace: {err}.")
        linux_distribution_name = None
        linux_distribution_version = None

    return {
        "computer_network_name": platform.node(),
        "operating_system_code": opersys,
        "processor_architecture": platform.machine(),
        # custom Linux
        "linux_distribution_name": linux_distribution_name,
        "linux_distribution_version": linux_distribution_version,
        # custom Windows
        "windows_edition": platform.win32_edition(),
    }
