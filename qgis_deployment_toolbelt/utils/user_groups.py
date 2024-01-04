#! python3  # noqa: E265

"""
    Utilities to manage user security groups either on Linux and Windows.

    Author: Julien Moura (https://github.com/guts)
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import logging
from functools import lru_cache
from getpass import getuser
from platform import uname
from sys import platform as opersys

# Imports depending on operating system
if opersys == "win32":
    """windows"""

    # 3rd party
    import win32net
    import win32security
else:
    import grp

# #############################################################################
# ########## Globals ###############
# ##################################

logger = logging.getLogger(__name__)


# #############################################################################
# ########## Functions #############
# ##################################


@lru_cache
def get_user_local_groups(user_name: str | None = None) -> list[str]:
    """_summary_

    Args:
        user_name (str | None, optional): _description_. Defaults to None.

    Raises:
        NotImplementedError: _description_

    Returns:
        list[str]: _description_
    """
    if user_name is None:
        user_name = getuser()

    if opersys.lower() in ("darwin", "linux"):
        return [g.gr_name for g in grp.getgrall() if user_name in g.gr_mem]
    elif opersys.lower() in ("win32", "windows"):
        server_host_name = uname()[1]
        return win32net.NetUserGetLocalGroups(
            serverName=server_host_name, userName=user_name
        )
    else:
        raise NotImplementedError(f"Unsupported operating system: {opersys}")


@lru_cache
def is_user_in_group(group_name: str, user_name: str | None = None) -> bool:
    """
    Check if a user is a member of a specified group.

    Args:
        user_name (str | None, optional): The username to check.. Defaults to None.
        group_name (str): The name of the group to check membership.

    Returns:
        bool: True if the user is a member of the group, False otherwise.
    """
    if user_name is None:
        user_name = getuser()

    try:
        if opersys.lower() in ("darwin", "linux"):
            # Get the list of group names the user is a member of
            local_groups = get_user_local_groups()
            logger.debug(
                f"{user_name} belongs to following LOCAL groups: {'; '.join(local_groups)}. "
            )
            return group_name in local_groups
        elif opersys.lower() in ("win32", "windows"):
            local_groups = get_user_local_groups()
            logger.debug(
                f"{user_name} belongs to following LOCAL groups: {'; '.join(local_groups)}. "
            )

            domain = None  # Set to the appropriate domain or leave as None for the current domain

            user_info = win32net.NetUserGetInfo(domain, user_name, 1)
            # user_sid = user_info.get("user_sid")

            group_sid = win32security.LookupAccountName(domain, group_name)[0]

            return win32security.CheckTokenMembership(None, group_sid)

        else:
            raise NotImplementedError(f"Unsupported operating system: {opersys}")

    except KeyError as err:
        logger.error(
            f"The specified user '{user_name}' or the specified group "
            f"'{group_name}' does not exist. Trace: {err}"
        )
        return False
    except Exception as err:
        logger.critical(
            f"Checking if user '{user_name}' belongs to the group '{group_name}' failed. Trace: {err}"
        )
        return False
