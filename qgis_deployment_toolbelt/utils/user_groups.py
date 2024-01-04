#! python3  # noqa: E265

"""
    Utilities to manage user security groups either on Linux and Windows.

    Author: Julien Moura (https://github.com/guts)
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import grp
import logging
from functools import lru_cache
from sys import platform as opersys

# Imports depending on operating system
if opersys == "win32":
    """windows"""

    # 3rd party
    import win32net
    import win32security


# #############################################################################
# ########## Globals ###############
# ##################################

logger = logging.getLogger(__name__)


# #############################################################################
# ########## Functions #############
# ##################################


@lru_cache
def is_user_in_group(username: str, group_name: str) -> bool:
    """
    Check if a user is a member of a specified group.

    Args:
        username (str): The username to check.
        group_name (str): The name of the group to check membership.

    Returns:
        bool: True if the user is a member of the group, False otherwise.
    """
    try:
        if opersys.lower() in ("darwin", "linux"):
            # Get the list of group names the user is a member of
            groups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
            logger.debug(
                f"{username} belongs to follwing groups: {'; '.join(groups)}. "
            )
            return group_name in groups
        elif opersys.lower() in ("win32", "windows"):
            domain = None  # Set to the appropriate domain or leave as None for the current domain

            user_info = win32net.NetUserGetInfo(domain, username, 1)
            # user_sid = user_info.get("user_sid")

            group_sid = win32security.LookupAccountName(domain, group_name)[0]

            return win32security.CheckTokenMembership(None, group_sid)

        else:
            raise NotImplementedError(f"Unsupported operating system: {opersys}")

    except KeyError as err:
        logger.error(
            f"The specified user '{username}' or the specified group "
            f"'{group_name}' does not exist. Trace: {err}"
        )
        return False
    except Exception as err:
        logger.critical(
            f"Checking if user '{username}' belongs to the group '{group_name}' failed. Trace: {err}"
        )
        return False
