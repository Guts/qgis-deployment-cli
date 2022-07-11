#! python3  # noqa: E265

"""
    Download remote QGIS profiles to local.

    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from os.path import expanduser, expandvars
from pathlib import Path
from shutil import copy2, copytree
from sys import platform as opersys
from typing import Tuple

# package
from qgis_deployment_toolbelt.constants import OS_CONFIG
from qgis_deployment_toolbelt.profiles import RemoteGitHandler

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################


class JobProfilesDownloader:
    """
    Job to download remote profiles and set them.
    """

    ID: str = "qprofiles-manager"
    OPTIONS_SCHEMA: dict = {
        "action": {
            "type": str,
            "required": False,
            "default": "download",
            "possible_values": ("download", "refresh"),
            "condition": "in",
        },
        "local_destination": {
            "type": str,
            "required": False,
            "default": ".cache/qgis-deployment-toolbelt/profiles",
            "possible_values": None,
            "condition": None,
        },
        "protocol": {
            "type": str,
            "required": True,
            "default": "http",
            "possible_values": ("http", "git", "copy"),
            "condition": "in",
        },
        "source": {
            "type": str,
            "required": True,
            "default": None,
            "possible_values": ("https://", "http://", "git://", "file://"),
            "condition": "startswith",
        },
    }
    PROFILES_NAMES_DOWNLOADED: list = []
    PROFILES_NAMES_INSTALLED: list = []

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
        self.qgis_profiles_path: Path = Path(OS_CONFIG.get(opersys).profiles_path)
        if not self.qgis_profiles_path.exists():
            logger.warning(
                f"QGIS profiles folder not found: {self.qgis_profiles_path}. "
                "Creating it to properly run the job."
            )
            self.qgis_profiles_path.mkdir(parents=True)

        # TODO: handle custom profiles folder through QGIS_CUSTOM_CONFIG_PATH

        # list installed profiles
        self.PROFILES_NAMES_INSTALLED = [
            d.name
            for d in self.qgis_profiles_path.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        ]

        # prepare local destination
        self.local_path: Path = Path(
            expandvars(expanduser(self.options.get("local_destination")))
        )
        if not self.local_path.exists():
            self.local_path.mkdir(parents=True, exist_ok=True)

    def run(self) -> None:
        """Execute job logic."""
        # download or refresh
        if self.options.get("action") != "download":
            raise NotImplementedError

        # prepare remote source
        if self.options.get("protocol") == "git":
            downloader = RemoteGitHandler(url=self.options.get("source"))
            downloader.clone_or_pull(self.local_path)
        else:
            raise NotImplementedError

        # check of there are some profiles folders within the downloaded folder
        profiles_folders = self.filter_profiles_folder()
        if profiles_folders is None:
            logger.error("No QGIS profile found in the downloaded folder.")
            return

        # store downloaded profiles names
        self.PROFILES_NAMES_DOWNLOADED = [d.name for d in profiles_folders]
        logger.info(
            f"{len(self.PROFILES_NAMES_DOWNLOADED)} downloaded profiles: "
            f"{', '.join(self.PROFILES_NAMES_DOWNLOADED)}"
        )

        # copy profiles to the QGIS 3
        self.sync_local_profiles(source_profiles_folder=profiles_folders)

        logger.debug(f"Job {self.ID} ran successfully.")

    def filter_profiles_folder(self) -> Tuple[Path] or None:
        """Parse downloaded folder to filter on QGIS profiles folders.

        :return Tuple[Path] or None: tuple of profiles folders paths
        """
        # first, try to get folders containing a profile.json
        qgis_profiles_folder = [
            f.parent for f in self.local_path.glob("**/profile.json")
        ]
        if len(qgis_profiles_folder):
            return tuple(qgis_profiles_folder)

        # if empty, try to identify if a folder is a QGIS profile - but unsure
        for d in self.local_path.glob("**"):
            if (
                d.is_dir()
                and d.parent.name == "profiles"
                and not d.name.startswith(".")
            ):
                qgis_profiles_folder.append(d)

        if len(qgis_profiles_folder):
            return tuple(qgis_profiles_folder)

        # if still empty, raise a warning but returns every folder under a `profiles` folder
        # TODO: try to identify if a folder is a QGIS profile with some approximate criteria

        if len(qgis_profiles_folder):
            logger.error("No QGIS profile found in the downloaded folder.")
            return None

    def sync_local_profiles(self, source_profiles_folder: tuple) -> None:
        """Copy downloaded profiles to QGIS profiles folder.
        If the QGIS profiles folder doesn't exist, it will be created and every
        downloaded profile will be copied.
        If a profile is already installed, it won't be overwritten.

        :param tuple source_profiles_folder: list of downloaded profiles folders paths
        """
        # check if local profiles folder exists or it's empty
        if not self.qgis_profiles_path.exists() or not any(
            self.qgis_profiles_path.iterdir()
        ):
            # ensure it exists
            self.qgis_profiles_path.mkdir(parents=True, exist_ok=True)
            # copy downloaded profiles into this
            for d in source_profiles_folder:
                copytree(
                    d,
                    self.qgis_profiles_path,
                    copy_function=copy2,
                    dirs_exist_ok=True,
                )
        elif len(
            set(self.PROFILES_NAMES_DOWNLOADED) - set(self.PROFILES_NAMES_INSTALLED)
        ):
            already_installed = [
                p
                for p in self.PROFILES_NAMES_DOWNLOADED
                if p in self.PROFILES_NAMES_INSTALLED
            ]
            not_installed = [
                p
                for p in self.PROFILES_NAMES_DOWNLOADED
                if p not in self.PROFILES_NAMES_INSTALLED
            ]

            logger.error(
                "Mixed case. "
                f"Already installed profiles: {','.join(already_installed)}. "
                f"Not installed: {','.join(not_installed)}."
            )

            for d in source_profiles_folder:
                if d.name in not_installed:
                    # create destination parent folder
                    to_profile_parent_folderpath = Path(
                        self.qgis_profiles_path / d.name
                    )
                    to_profile_parent_folderpath.mkdir(parents=True, exist_ok=True)
                    copytree(
                        d,
                        to_profile_parent_folderpath,
                        copy_function=copy2,
                        dirs_exist_ok=True,
                    )

        else:
            logger.error(
                "QGIS Profiles folder already exists, it's not empty: "
                f"{self.qgis_profiles_path.resolve()}"
            )

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
