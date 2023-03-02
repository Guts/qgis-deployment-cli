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
    OPTIONS_SCHEMA: dict = {
        "action": {
            "type": str,
            "required": False,
            "default": "add",
            "possible_values": ("add", "remove"),
            "condition": "in",
        },
        "name": {
            "type": str,
            "required": True,
            "default": None,
            "possible_values": None,
            "condition": None,
        },
        "scope": {
            "type": str,
            "required": False,
            "default": "user",
            "possible_values": ("system", "user"),
            "condition": "in",
        },
        "value": {
            "type": (bool, int, str, list),
            "required": False,
            "default": None,
            "possible_values": None,
            "condition": None,
        },
    }

    def __init__(self, options: List[dict]) -> None:
        """Instantiate the class.

        Args:
            options (List[dict]): list of dictionary with environment variables to set
            or remove.
        """
        self.options: List[dict] = [self.validate_options(opt) for opt in options]

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

    # -- INTERNAL LOGIC ------------------------------------------------------
    def validate_options(self, options: dict) -> dict:
        """Validate options.

        Args:
            options (dict): options to validate.

        Raises:
            ValueError: if option has an invalid name or doesn't comply with condition
            TypeError: if the option does'nt not comply with expected type

        Returns:
            dict: options if valid
        """
        for option in options:
            if option not in self.OPTIONS_SCHEMA:
                raise ValueError(
                    f"Job: {self.ID}. Option '{option}' is not valid."
                    f" Valid options are: {self.OPTIONS_SCHEMA.keys()}"
                )

            option_in = options.get(option)
            option_def: dict = self.OPTIONS_SCHEMA.get(option)
            # check value type
            if not isinstance(option_in, option_def.get("type")):
                raise TypeError(
                    f"Job: {self.ID}. Option '{option}' has an invalid value."
                    f"\nExpected {option_def.get('type')}, got {type(option_in)}"
                )
            # check value condition
            if option_def.get("condition") == "startswith" and not option_in.startswith(
                option_def.get("possible_values")
            ):
                raise ValueError(
                    f"Job: {self.ID}. Option '{option}' has an invalid value."
                    "\nExpected: starts with one of: "
                    f"{', '.join(option_def.get('possible_values'))}"
                )
            elif option_def.get(
                "condition"
            ) == "in" and option_in not in option_def.get("possible_values"):
                raise ValueError(
                    f"Job: {self.ID}. Option '{option}' has an invalid value."
                    f"\nExpected: one of: {', '.join(option_def.get('possible_values'))}"
                )
            else:
                pass

        return options


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
