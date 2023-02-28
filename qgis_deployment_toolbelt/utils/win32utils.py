#! python3  # noqa: E265

"""
    Utilities specific for Windows.

    Author: Julien Moura (https://github.com/guts)

    Inspired from py-setenv: <https://github.com/beliaev-maksim/py_setenv> (MIT)
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from os import sep  # required since pathlib strips trailing whitespace
from pathlib import Path
from sys import platform as opersys
from typing import Optional

# Imports depending on operating system
if opersys == "win32":
    """windows"""

    import winreg

    import win32gui
else:
    pass


# #############################################################################
# ########## Globals ###############
# ##################################

logger = logging.getLogger(__name__)

if opersys == "win32":
    """windows"""
    system_hkey = (
        winreg.HKEY_LOCAL_MACHINE,
        r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
    )
    user_hkey = (winreg.HKEY_CURRENT_USER, r"Environment")

# #############################################################################
# ########## Functions #############
# ##################################


def delete_environment_variable(envvar_name: str, scope: str = "user") -> bool:
    """Deletes environment variable.

    Args:
        envvar_name (str): environment variable name (= key) to delete
        scope (str, optional): environment variable scope. Must be "user" or "system",
            defaults to "user". Defaults to "user".

    Returns:
        bool: True is the variable has been successfully deleted
    """
    # user or system
    if scope == "user":
        hkey = user_hkey
    else:
        system_hkey

    # get it to check if variable exits
    try:
        get_environment_variable(envvar_name=envvar_name, scope=scope)
    except Exception:
        return False

    # try to delete the variable
    try:
        with winreg.OpenKey(*hkey, access=winreg.KEY_ALL_ACCESS) as key:
            winreg.DeleteValue(key, envvar_name)
            return True
    except OSError as err:
        logger.error(
            f"Delete variable '{envvar_name}' from scope '{scope}' failed. Trace: {err}"
        )
        return False


def get_environment_variable(envvar_name: str, scope: str = "user") -> Optional[str]:
    """Get environment variable from Windows registry.

    Args:
        envvar_name (str): environment variable name (= key) to retrieve
        scope (str, optional): environment variable scope. Must be "user" or "system",
            defaults to "user". Defaults to "user".

    Returns:
        Optional[str]: environment variable value or None if not found
    """
    # user or system
    if scope == "user":
        hkey = user_hkey
    else:
        system_hkey
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


def normalize_path(input_path: Path, add_trailing_slash_if_dir: bool = True) -> str:
    r"""Returns a path as normalized and fully escaped for Windows old-school file style.

    :param Path input_path: path to normalize
    :param bool add_trailing_slash_if_dir: add a trailing slash if the input is a folder,\
        defaults to True

    :return str: normalized path as string

    :example:

    .. code-block:: python

        t = Path(r'C:\Users\risor\Documents\GitHub\Geotribu\qtribu\qtribu\resources\images')
        print(normalize_path(t))
        > C:\\Users\\risor\\Documents\\GitHub\\Geotribu\\qtribu\\qtribu\\resources\\images\\

    """
    if input_path.is_dir() and add_trailing_slash_if_dir:
        return repr(str(input_path.resolve()) + sep).replace("'", "")
    else:
        return repr(str(input_path.resolve())).replace("'", "")


def refresh_environment() -> bool:
    """This ensures that changes to Windows registry are immediately propagated.
    Useful to refresh after have updated the environment variables.

    A method by Geoffrey Faivre-Malloy and Ronny Lipshitz.
    Source: https://gist.github.com/apetrone/5937002

    Returns:
        bool: True if the environment has been refreshed
    """
    # broadcast settings change
    HWND_BROADCAST: int = 0xFFFF
    WM_SETTINGCHANGE: int = 0x001A
    SMTO_ABORTIFHUNG: int = 0x0002
    sParam = "Environment"

    res1 = res2 = None
    try:
        res1, res2 = win32gui.SendMessageTimeout(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0, sParam, SMTO_ABORTIFHUNG, 100
        )
    except NameError:
        logger.critical(" name 'win32gui' is not defined")
    if not res1:
        logger.warning(
            f"Refresh environment failed: {bool(res1)}, {res2}, from SendMessageTimeout"
        )
        return False
    else:
        return True


def set_environment_variable(
    envvar_name: str, envvar_value: str, scope: str = "user"
) -> bool:
    """Creates/replaces environment variable.

    Args:
        envvar_name (str): name (= key) of environment variable to set or replace.
        envvar_value (str): value to set for the environment variable
        scope (str, optional): environment variable scope. Must be "user" or "system",
            defaults to "user". Defaults to "user".

    Returns:
        bool: True is the variable has been successfully set
    """
    # user or system
    if scope == "user":
        hkey = user_hkey
    else:
        system_hkey

    # try to set the value
    try:
        with winreg.OpenKey(*hkey, access=winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, envvar_name, 0, winreg.REG_SZ, envvar_value)
        return True
    except OSError as err:
        logger.error(
            f"Set variable '{envvar_name}' with value '{envvar_value}' to "
            f"scope '{scope}' failed. Trace: {err}"
        )
        return False


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    # pass
    t = Path("C:/Users/risor/Documents/GitHub/Geotribu/qtribu/qtribu/resources/images")
    print(normalize_path(t))
