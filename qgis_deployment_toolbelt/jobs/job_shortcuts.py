#! python3  # noqa: E265

"""
    Manage application shortcuts on end-user machine.

    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from os.path import expandvars
from pathlib import Path
from sys import platform as opersys
from typing import Tuple, Union

# package
from qgis_deployment_toolbelt.__about__ import __title__, __version__
from qgis_deployment_toolbelt.constants import OS_CONFIG
from qgis_deployment_toolbelt.profiles import ApplicationShortcut

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################


class JobShortcutsManager:
    """
    Job to create or remove shortcuts on end-user machine.
    """

    ID: str = "shortcuts-manager"
    OPTIONS_SCHEMA: dict = {
        "action": {
            "type": str,
            "required": False,
            "default": "create",
            "possible_values": ("create", "create_or_restore", "remove"),
            "condition": "in",
        },
        "include": {
            "type": (list, str),
            "required": False,
            "default": None,
            "possible_values": None,
            "condition": None,
            "sub_options": {
                "additional_arguments": {
                    "type": str,
                    "required": False,
                    "default": None,
                    "possible_values": None,
                    "condition": None,
                },
                "desktop": {
                    "type": bool,
                    "required": False,
                    "default": False,
                    "possible_values": None,
                    "condition": None,
                },
                "icon": {
                    "type": str,
                    "required": False,
                    "default": None,
                    "possible_values": None,
                    "condition": None,
                },
                "label": {
                    "type": str,
                    "required": False,
                    "default": "QGIS",
                    "possible_values": None,
                    "condition": None,
                },
                "profile": {
                    "type": str,
                    "required": True,
                    "default": None,
                    "possible_values": None,
                    "condition": None,
                },
                "start_menu": {
                    "type": bool,
                    "required": False,
                    "default": True,
                    "possible_values": None,
                    "condition": None,
                },
            },
        },
    }
    SHORTCUTS_CREATED: list = []
    SHORTCUTS_REMOVED: list = []

    def __init__(self, options: dict) -> None:
        """Instantiate the class.

        :param dict options: profiles source (remote, can be a local network) and
        destination (local).
        """
        self.options: dict = self.validate_options(options)

        # profile folder
        if opersys not in OS_CONFIG:
            raise OSError(
                f"Your operating system {opersys} is not supported. "
                f"Supported platforms: {','.join(OS_CONFIG.keys())}."
            )

    def run(self) -> None:
        """Execute job logic."""
        # check action
        if self.options.get("action") in ("create", "create_or_restore"):
            for p in self.options.get("include", []):
                shortcut = ApplicationShortcut(
                    name=p.get("label"),
                    exec_path=Path(expandvars(p.get("qgis_path"))),
                    description=f"Created with {__title__} {__version__}",
                    icon_path=self.get_icon_path(p.get("icon"), p.get("profile")),
                    exec_arguments=self.get_arguments_ready(
                        p.get("profile"), p.get("additional_arguments")
                    ),
                    work_dir=Path().home() / "Documents",
                )
                shortcut.create(
                    desktop=p.get("desktop", False),
                    start_menu=p.get("start_menu", True),
                )
                logger.info(f"Created shortcut {shortcut.name}")
                self.SHORTCUTS_CREATED.append(shortcut)

            logger.debug(f"Job {self.ID} ran successfully.")
        else:
            raise NotImplementedError

    # -- INTERNAL LOGIC ------------------------------------------------------
    def get_icon_path(self, icon: str, profile_name: str) -> Union[Path, None]:
        """Try to get icon path.

        First, right next to the toolbelt;
        then under a subfolder starting from the toolbelt (adn handling pathlib OSError);
        if still not, within the related profile folder.
        None as fallback.

        :param str icon: icon path as mentioned into the scenario file
        :param str profile_name: QGIS profile name where to look into
        :return Union[Path, None]: _description_
        """
        # try to get icon right aside the toolbelt
        if Path(icon).is_file():
            logger.debug(f"Icon found next to the toolbelt: {Path(icon).resolve()}")
            return Path(icon).resolve()

        # try to get icon within folders under toolbelt
        try:
            li_subfolders = list(Path(".").rglob(f"{icon}"))
            if len(li_subfolders):
                logger.debug(
                    f"Icon found under the toolbelt: {li_subfolders[0].resolve()}"
                )
                return li_subfolders[0].resolve()
        except OSError as err:
            logger.error(
                "Looking for icon within folders under toolbelt failed. %s" % err
            )

        # try to get icon within profile folder
        qgis_profile_path: Path = Path(
            OS_CONFIG.get(opersys).profiles_path / profile_name
        )
        if qgis_profile_path.is_dir():
            li_subfolders = list(qgis_profile_path.rglob(f"{icon}"))
            if len(li_subfolders):
                logger.debug(
                    f"Icon found within profile folder: {li_subfolders[0].resolve()}"
                )
                return li_subfolders[0].resolve()

        return None

    def get_arguments_ready(self, profile: str, in_arguments: str = None) -> Tuple[str]:
        """Prepare arguments for the executable shortcut.

        :param list in_arguments: argument as defined in the scenario file

        :return Tuple[str]: tuple of strings separated by spaces
        """
        # add profile name
        arguments: list = ["--profile", profile]

        # add additional arguments
        if in_arguments:
            arguments.extend(in_arguments.split(" "))

        return arguments

    def validate_options(self, options: dict) -> bool:
        """Validate options.

        :param dict options: options to validate.
        :return bool: True if options are valid.
        """
        for option in options:
            if option not in self.OPTIONS_SCHEMA:
                raise Exception(
                    f"Job: {self.ID}. Option '{option}' is not valid."
                    f" Valid options are: {self.OPTIONS_SCHEMA.keys()}"
                )

            option_in = options.get(option)
            option_def: dict = self.OPTIONS_SCHEMA.get(option)
            # check value type
            if not isinstance(option_in, option_def.get("type")):
                raise Exception(
                    f"Job: {self.ID}. Option '{option}' has an invalid value."
                    f"\nExpected {option_def.get('type')}, got {type(option_in)}"
                )
            # check value condition
            if option_def.get("condition") == "startswith" and not option_in.startswith(
                option_def.get("possible_values")
            ):
                raise Exception(
                    f"Job: {self.ID}. Option '{option}' has an invalid value."
                    "\nExpected: starts with one of: "
                    f"{', '.join(option_def.get('possible_values'))}"
                )
            elif option_def.get(
                "condition"
            ) == "in" and option_in not in option_def.get("possible_values"):
                raise Exception(
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
