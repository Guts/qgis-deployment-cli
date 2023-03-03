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
from pathlib import Path
from shutil import copy2, copytree
from sys import platform as opersys
from typing import Tuple

# package
from qgis_deployment_toolbelt.constants import OS_CONFIG, get_qdt_working_directory
from qgis_deployment_toolbelt.jobs.generic_job import GenericJob
from qgis_deployment_toolbelt.profiles import RemoteGitHandler

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################


class JobProfilesDownloader(GenericJob):
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
        "branch": {
            "type": str,
            "required": False,
            "default": "master",
            "possible_values": None,
            "condition": None,
        },
        "source": {
            "type": str,
            "required": True,
            "default": None,
            "possible_values": ("https://", "http://", "git://", "file://"),
            "condition": "startswith",
        },
        "sync_mode": {
            "type": str,
            "required": False,
            "default": "only_missing",
            "possible_values": (
                "only_missing",
                "only_different_version",
                "only_new_version",
                "overwrite",
            ),
            "condition": "in",
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

        # local QDT folder
        self.qdt_working_folder = get_qdt_working_directory()
        logger.debug(f"Working folder: {self.qdt_working_folder}")

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
        if not self.qdt_working_folder.exists():
            self.qdt_working_folder.mkdir(parents=True, exist_ok=True)

    def run(self) -> None:
        """Execute job logic."""
        # download or refresh
        if self.options.get("action") != "download":
            raise NotImplementedError

        # prepare remote source
        if self.options.get("protocol") == "git":
            downloader = RemoteGitHandler(
                url=self.options.get("source"),
                branch=self.options.get("branch", "master"),
            )
            downloader.download(local_path=self.qdt_working_folder)
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
            f.parent for f in self.qdt_working_folder.glob("**/profile.json")
        ]
        if len(qgis_profiles_folder):
            return tuple(qgis_profiles_folder)

        # if empty, try to identify if a folder is a QGIS profile - but unsure
        for d in self.qdt_working_folder.glob("**"):
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

    def sync_local_profiles(self, source_profiles_folder: Tuple[Path]) -> None:
        """Copy downloaded profiles to QGIS profiles folder.
        If the QGIS profiles folder doesn't exist, it will be created and every
        downloaded profile will be copied.
        If a profile is already installed, it won't be overwritten.

        :param Tuple[Path] source_profiles_folder: list of downloaded profiles folders paths
        """
        # check if local profiles folder exists or it's empty
        if not self.qgis_profiles_path.exists() or not any(
            self.qgis_profiles_path.iterdir()
        ):
            logger.info(
                "The QGIS profiles folder does not exist or is empty: "
                f"{self.qgis_profiles_path.resolve()}. Probably a fresh install."
                "Copying downloaded profiles..."
            )
            # ensure QGIS profiles folder exists
            self.qgis_profiles_path.mkdir(parents=True, exist_ok=True)

            # copy all downloaded profiles
            self.sync_overwrite_local_profiles(
                profiles_folder_to_copy=source_profiles_folder
            )

        elif (
            len(
                set(self.PROFILES_NAMES_DOWNLOADED) - set(self.PROFILES_NAMES_INSTALLED)
            )
            and self.options.get("sync_mode") == "only_missing"
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
            logger.debug(
                "QGIS Profiles folder already exists, it's not empty: "
                f"{self.qgis_profiles_path.resolve()}"
            )

    def sync_copy_only_missing(self, profiles_folder_to_copy: Tuple[Path]) -> None:
        """Copy only missing profiles from downloaded ones to QGIS profiles folder to
        local destination."""
        # copy downloaded profiles into this
        for d in profiles_folder_to_copy:
            copytree(
                d,
                self.qgis_profiles_path,
                copy_function=copy2,
                dirs_exist_ok=True,
            )

    def sync_overwrite_local_profiles(
        self, profiles_folder_to_copy: Tuple[Path]
    ) -> None:
        """Overwrite local profiles with downloaded ones."""
        # ensure QGIS profiles folder exists
        self.qgis_profiles_path.mkdir(parents=True, exist_ok=True)
        # copy downloaded profiles into this
        for d in profiles_folder_to_copy:
            copytree(
                d,
                self.qgis_profiles_path,
                copy_function=copy2,
                dirs_exist_ok=True,
            )


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
