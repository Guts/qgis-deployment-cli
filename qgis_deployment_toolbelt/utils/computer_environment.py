#! python3  # noqa: E265

"""
    Rules context.

    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
import platform
from datetime import date
from getpass import getuser
from sys import platform as opersys

# package
from qgis_deployment_toolbelt.utils.user_groups import (
    get_user_domain_groups,
    get_user_local_groups,
)

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Functions #############
# ##################################


def date_dict() -> dict:
    """Returns a context dictionary with date informations that can be used in QDT
    various places: rules...

    Returns:
        dict: dict with current date informations
    """
    today = date.today()
    return {
        "current_day": today.day,
        "current_weekday": today.weekday(),  # monday = 0, sunday = 6
        "current_month": today.month,
        "current_year": today.year,
    }


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


def user_dict() -> dict:
    """Returns a dictionary containing user informations that can be used in QDT Rules
        context.

    Returns:
        dict: dict user information.
    """
    return {
        "name": getuser(),
        "groups_local": get_user_local_groups(),
        "groups_domain": get_user_domain_groups(),
    }
