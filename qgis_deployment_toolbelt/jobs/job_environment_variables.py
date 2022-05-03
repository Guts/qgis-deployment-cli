#! python3  # noqa: E265

"""
    Tools to manage the environment setup (variables, etc.)

    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from sys import platform as opersys

# Imports depending on operating system
if opersys == "win32":
    """windows"""
    import win32gui
    from py_setenv import setenv
else:
    pass

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################


class JobEnvironmentVariables:
    """
    Class to manage the environment variables of QGIS installation.
    """

    ID: str = "manage-env-vars"
    WINDOWS: bool = opersys == "win32"

    def __init__(self, options: dict) -> None:
        """Instantiate the class.

        :param dict options: dictionary with environment variable name as key and
        some parameters as values (value, scope, action...).
        """
        self.options: dict = options

    def run(self) -> None:
        """Apply environment variables from dictionary to the system."""
        if self.WINDOWS:
            for env_var, var_params in self.options.items():
                if var_params[2] == "add":
                    setenv(
                        name=env_var,
                        value=var_params[0],
                        user=var_params[1] == "user",
                        suppress_echo=True,
                    )
            self.win_refresh_environment()

        # TODO: for linux, edit ~/.profile or add a .env file and source it from ~./profile
        else:
            logger.debug(
                f"Setting persistent environment variables is not supported on {opersys}"
            )

        logger.debug(f"Job {self.ID} ran successfully.")

    def win_refresh_environment(self) -> bool:
        """This ensures that changes to Windows registry are immediately propagated.
        Useful to refresh after have updated the environment variables.

        A method by Geoffrey Faivre-Malloy and Ronny Lipshitz.
        Source: https://gist.github.com/apetrone/5937002

        :return bool: True if the environment has been refreshed
        """
        # broadcast settings change
        HWND_BROADCAST: int = 0xFFFF
        WM_SETTINGCHANGE: int = 0x001A
        SMTO_ABORTIFHUNG: int = 0x0002
        sParam = "Environment"

        res1, res2 = win32gui.SendMessageTimeout(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0, sParam, SMTO_ABORTIFHUNG, 100
        )
        if not res1:
            logger.warning(
                f"Refresh environment failed: {bool(res1)}, {res2}, from SendMessageTimeout"
            )
            return False
        else:
            return True


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
