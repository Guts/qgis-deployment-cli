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
from os.path import expanduser, expandvars
from pathlib import Path
from sys import platform as opersys
from typing import List

# package
from qgis_deployment_toolbelt.utils.win32utils import (
    delete_environment_variable,
    refresh_environment,
    set_environment_variable,
)

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

    def __init__(self, options: List[dict]) -> None:
        """Instantiate the class.

        Args:
            options (List[dict]): dictionary with environment variable name as key and
        some parameters as values (value, scope, action...).
        """

        self.options: dict = self.validate_options(options)

    def run(self) -> None:
        """Apply environment variables from dictionary to the system."""
        if opersys == "win32":
            for env_var in self.options:
                if env_var.get("action") == "add":
                    try:
                        set_environment_variable(
                            envvar_name=env_var.get("name"),
                            envvar_value=self.prepare_value(env_var.get("value")),
                            scope=env_var.get("scope"),
                        )
                    except NameError:
                        logger.debug(
                            f"Variable name '{env_var.get('name')}' is not defined"
                        )
                elif env_var.get("action") == "remove":
                    try:
                        delete_environment_variable(
                            envvar_name=env_var.get("name"),
                            scope=env_var.get("scope"),
                        )
                    except NameError:
                        logger.debug(
                            f"Variable name '{env_var.get('name')}' is not defined"
                        )
            # force Windows to refresh the environment
            refresh_environment()

        # TODO: for linux, edit ~/.profile or add a .env file and source it from ~./profile
        else:
            logger.debug(
                f"Setting persistent environment variables is not supported on {opersys}"
            )

        logger.debug(f"Job {self.ID} ran successfully.")

    def prepare_value(self, value: str) -> str:
        """Prepare value to be used in the environment variable.

        :param str value: value to prepare.
        :return str: prepared value.
        """
        try:
            # test if value is a path
            value_as_path = Path(expanduser(expandvars(value)))
            if not value_as_path.exists():
                logger.warning(
                    f"{value} seems to be a valid path but does not exist (yet)."
                )

            return str(value_as_path.resolve())
        except Exception as err:
            logger.debug(f"Value {value} is not a valid path: {err}")

        return str(value).strip()

    def validate_options(self, options: List[dict]) -> List[dict]:
        """Validate options.

        :param List[dict] options: options to validate.
        :return List[dict]: options if they are valid.
        """
        if not isinstance(options, list):
            raise TypeError(f"Options must be a list, not {type(options)}")
        for option in options:
            if not isinstance(option, dict):
                raise TypeError(f"Options must be a dict, not {type(option)}")

        return options


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
