#! python3  # noqa: E265

"""
    Utilities specific for Windows.

    Author: Julien Moura (https://github.com/guts)
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from sys import platform as opersys
from typing import Union

# Imports depending on operating system
if opersys == "win32":
    """windows"""
    import winreg
else:
    pass

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Functions #############
# ##################################
def get_environment_variable(envvar_name: str, scope: str = "user") -> Union[str, None]:
    """Get environment variable from Windows registry.

    :param str envvar_name: environment variable name to retrieve
    :param str scope: . Must be "user" or "system", defaults to "user".

    :return Union[str, None]: environment variable value or None if not found
    """
    # user or system
    if scope == "user":
        hkey = (winreg.HKEY_CURRENT_USER, r"Environment")
    else:
        hkey = (
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
        )
    # try to get the value
    try:
        with winreg.OpenKey(*hkey, access=winreg.KEY_READ) as key:
            value, regtype = winreg.QueryValueEx(key, envvar_name)
        return value
    except OSError:
        logger.error(
            f"Environment variable {envvar_name} not found in registry (scope: {scope}"
        )
        return None


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
