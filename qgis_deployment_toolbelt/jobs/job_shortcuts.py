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
from pathlib import Path
from sys import platform as opersys

# package
from qgis_deployment_toolbelt.__about__ import __title__, __version__
from qgis_deployment_toolbelt.constants import OS_CONFIG, get_qdt_working_directory
from qgis_deployment_toolbelt.jobs.generic_job import GenericJob
from qgis_deployment_toolbelt.profiles import ApplicationShortcut
from qgis_deployment_toolbelt.profiles.qdt_profile import QdtProfile
from qgis_deployment_toolbelt.utils.check_path import check_path

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################


class JobShortcutsManager(GenericJob):
    """
    Job to create or remove shortcuts on end-user machine.
    """

    ID: str = "shortcuts-manager"
    OPTIONS_SCHEMA: dict = {
        "action": {
            "type": str,
            "required": False,
            "default": "create_or_restore",
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

        self.os_config = OS_CONFIG.get(opersys)
        self.qdt_working_folder = get_qdt_working_directory()
        self.qgis_profiles_path: Path = Path(self.os_config.profiles_path)

    def run(self) -> None:
        """Execute job logic."""
        # check action
        if self.options.get("action") in ("create", "create_or_restore"):
            for p in self.options.get("include", []):
                shortcut = ApplicationShortcut(
                    name=p.get("label"),
                    exec_path=self.get_qgis_path(p.get("qgis_path")),
                    description=f"Created with {__title__} {__version__}",
                    icon_path=self.get_icon_path(p.get("icon"), p.get("profile")),
                    exec_arguments=self.get_arguments_ready(
                        p.get("profile"), p.get("additional_arguments")
                    ),
                    work_dir=self.get_profile_folder_path_from_name(
                        p.get("profile", "default")
                    ),
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

    def filter_profiles_folder(self) -> tuple[QdtProfile]:
        """Parse downloaded folder to filter on QGIS profiles folders.

        Returns:
            tuple[QdtProfile]: tuple of profiles objects
        """
        # first, try to get folders containing a profile.json
        qgis_profiles_folder = [
            QdtProfile.from_json(profile_json_path=f, profile_folder=f.parent)
            for f in self.qdt_working_folder.glob("**/profile.json")
        ]
        if len(qgis_profiles_folder):
            logger.debug(
                f"{len(qgis_profiles_folder)} profiles found within {self.qdt_working_folder}"
            )
            return tuple(qgis_profiles_folder)

        # if empty, try to identify if a folder is a QGIS profile - but unsure
        for d in self.qdt_working_folder.glob("**"):
            if (
                d.is_dir()
                and d.parent.name == "profiles"
                and not d.name.startswith(".")
            ):
                qgis_profiles_folder.append(QdtProfile(folder=d, name=d.name))

        if len(qgis_profiles_folder):
            return tuple(qgis_profiles_folder)

        # if still empty, raise a warning but returns every folder under a `profiles` folder
        # TODO: try to identify if a folder is a QGIS profile with some approximate criteria

        if not len(qgis_profiles_folder):
            logger.error("No QGIS profile found in the downloaded folder.")
            return None

    def get_profile_folder_path_from_name(self, profile_name: str) -> Path:
        """Determine profile directory folder (once installed in QGIS) from the profile name.

        Args:
            profile_name (str): profile name

        Returns:
            Path: path to the profile folder
        """
        path_normal_case = Path(self.qgis_profiles_path, profile_name)

        if check_path(
            input_path=path_normal_case, must_be_a_folder=True, raise_error=False
        ):
            return path_normal_case
        else:
            path_lower_case = Path(self.qgis_profiles_path, profile_name.lower())
            if check_path(
                input_path=path_lower_case, must_be_a_folder=True, raise_error=False
            ):
                logger.warning(
                    f"Path to the profile folder doesn't exist: {path_normal_case}. "
                    f"But it does lowercasing the profile name: {path_lower_case}."
                    "Please amend the scenario file."
                )
                return path_lower_case
            else:
                logger.warning(
                    f"Path to the profile folder doesn't exist: {path_normal_case}, "
                    f"nor lowercasing the profile name: {path_lower_case}."
                )
                return path_normal_case

    def get_icon_path(self, icon: str, profile_name: str) -> Path:
        """Try to get icon path. First, check that an icon key has been specified in the scenario file;
        then, right next to the toolbelt;
        then under a subfolder starting from the toolbelt (adn handling pathlib OSError);
        if still not, within the related profile folder.
        None as fallback.

        :param str icon: icon path as mentioned into the scenario file
        :param str profile_name: QGIS profile name where to look into
        :return Union[Path, None]: icon path as Path if str or Path, else None
        """
        # try to get the value of the icon key
        if not icon:
            return None

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

    def get_arguments_ready(self, profile: str, in_arguments: str = None) -> tuple[str]:
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


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
