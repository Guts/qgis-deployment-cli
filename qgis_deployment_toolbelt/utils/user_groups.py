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
import subprocess
from functools import lru_cache
from getpass import getuser
from platform import uname
from sys import platform as opersys

# Imports depending on operating system
if opersys == "win32":
    """windows"""

    # 3rd party
    import win32com
    import win32net
    import win32security

    # try to import pyad
    try:
        import pyad
    except ImportError:
        logging.info("'pyad' package is not available.")
        pyad = None
    # try to import wmi
    try:
        import wmi
    except ImportError:
        logging.info("'wmi' package is not available. Trying to use wmi from win32com.")
        try:
            wmi = win32com.client.GetObject("winmgmts://./root/cimv2")
        except Exception as err:
            logging.error(
                "Unable to load WMI (Windows Management Instrumentation) from "
                f"win32com.client. Other options will be used. Trace: {err}"
            )
            wmi = None
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
    """Lists the local groups to which the user belong.

    On Linux and MacOS, it relies on the grp module (only available).
    On Windows, it relies on win32net (COM).

    Args:
        user_name (str | None, optional): name of user. If None, the current user name
            is used. Defaults to None.

    Raises:
        NotImplementedError: if operating system is not supported.

    Returns:
        list[str]: sorted list of unique groups names
    """
    if user_name is None:
        user_name = getuser()

    if opersys.lower() in ("darwin", "linux"):
        return sorted({g.gr_name for g in grp.getgrall() if user_name in g.gr_mem})
    elif opersys.lower() in ("win32", "windows"):
        server_host_name = uname()[1]
        return sorted(set(win32net.NetUserGetLocalGroups(server_host_name, user_name)))
    else:
        raise NotImplementedError(f"Unsupported operating system: {opersys}")


def _win32_is_computer_in_domain() -> bool:
    """Check if the computer is joined to a domain or a workgroup using WMI.

    Returns:
        bool: True if the computer is joined to a domain or workgroup, False otherwise.
    """
    try:
        # Connect to the WMI service
        wmi = win32com.client.GetObject("winmgmts://./root/cimv2")

        # Execute a query to retrieve information about the domain
        query = "SELECT * FROM Win32_ComputerSystem"
        result = wmi.ExecQuery(query)

        # Check if the domain attribute is not None
        for item in result:
            if item.Domain and item.Domain.lower() != "workgroup":
                return True

    except Exception as err:
        logger.error(f"Getting domain from WMI through win32com failed. Trace: {err}")
        raise err

    return False


@lru_cache
def is_computer_attached_to_a_domain() -> bool:
    """Determine if the computer is attached to a domain or not.

    On Linux and MacOS, it always return False.
    On Windows, it tries to use wmi (Windows Management Instrumentation), Active
        Directory (through pyad) or subprocessed powershell as final fallback.

    Raises:
        NotImplementedError: if operating system is not supported.

    Returns:
        bool: True if the computer is attached to a domain.
    """
    if opersys.lower() in ("darwin", "linux"):
        # TODO: find a way to determine if a computer is attached to a domain on Linux and MacOS
        return False
    elif opersys.lower() in ("win32", "windows"):
        if wmi is not None:
            if hasattr(wmi, "WMI"):
                try:
                    wmi_os = wmi.WMI().Win32_ComputerSystem()[0]
                    logger.info(
                        "Based on WMI, is the computer attached to a domain: "
                        f"{wmi_os.PartOfDomain}"
                    )
                    return wmi_os.PartOfDomain
                except Exception as err:
                    logger.error(
                        f"Something went wrong using WMI package. Trace: {err}"
                    )
            else:
                try:
                    return _win32_is_computer_in_domain()
                except Exception as err:
                    logger.error(
                        f"Something went wrong using WMI through win32com. Trace: {err}"
                    )

        if pyad is not None:
            try:
                user_obj = pyad.aduser.ADUser.from_cn(getuser())
                return bool(len(user_obj.get_attribute("memberOf")))
            except Exception as err:
                logger.info(
                    "Based on pyad, the current computer is not attached to any domain."
                    f" Trace: {err}"
                )
                return False

        # using PowerShell cmd through subprocess
        domain = subprocess.run(
            ["powershell.exe", "(Get-CimInstance Win32_ComputerSystem).Domain"],
            stdout=subprocess.PIPE,
            text=True,
        ).stdout.strip()
        return domain.lower() != "workgroup"

    else:
        raise NotImplementedError(f"Unsupported operating system: {opersys}")


@lru_cache
def is_user_in_group(group_name: str, user_name: str | None = None) -> bool:
    """Check if a user is a member of a specified group.

    Args:
        user_name (str | None, optional): The username to check. If None, the current
            user name is used. Defaults to None.
        group_name (str): The name of the group to check membership.

    Returns:
        bool: True if the user is a member of the group, False otherwise or if
            something fails.
    """
    if user_name is None:
        user_name = getuser()

    try:
        if opersys.lower() in ("darwin", "linux"):
            # Get the list of group names the user is a member of
            local_groups = get_user_local_groups()
            logger.debug(
                f"User '{user_name}' belongs to following LOCAL groups: "
                f"{'; '.join(local_groups)}. "
            )
            return group_name in local_groups
        elif opersys.lower() in ("win32", "windows"):
            local_groups = get_user_local_groups()
            logger.debug(
                f"User '{user_name}' belongs to following LOCAL groups: "
                f"{'; '.join(local_groups)}. "
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
            f"Checking if user '{user_name}' belongs to the group '{group_name}' "
            f"failed. Trace: {err}"
        )
        return False
