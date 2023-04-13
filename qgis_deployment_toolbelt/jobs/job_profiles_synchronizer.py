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
from collections.abc import Iterable
from pathlib import Path
from shutil import copy2, copytree
from sys import platform as opersys

# package
from qgis_deployment_toolbelt.constants import OS_CONFIG, get_qdt_working_directory
from qgis_deployment_toolbelt.jobs.generic_job import GenericJob
from qgis_deployment_toolbelt.profiles import LocalGitHandler, RemoteGitHandler
from qgis_deployment_toolbelt.profiles.qdt_profile import QdtProfile

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
        "branch": {
            "type": str,
            "required": False,
            "default": "master",
            "possible_values": None,
            "condition": None,
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

        Args:
            options (List[dict]): list of dictionary with environment variables to set
            or remove.
        """
        self.options: dict = self.validate_options(options)

        # local QDT folder
        self.qdt_working_folder = get_qdt_working_directory()
        logger.debug(f"Working folder: {self.qdt_working_folder}")

        # profile folder
        self.qgis_profiles_path: Path = Path(OS_CONFIG.get(opersys).profiles_path)
        if not self.qgis_profiles_path.exists():
            logger.warning(
                f"QGIS profiles folder not found: {self.qgis_profiles_path}. "
                "Creating it to properly run the job."
            )
            self.qgis_profiles_path.mkdir(exist_ok=True, parents=True)

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
            if self.options.get("source").startswith(("git://", "http://", "https://")):
                downloader = RemoteGitHandler(
                    uri_or_path=self.options.get("source"),
                    branch=self.options.get("branch", "master"),
                )
                downloader.download(local_path=self.qdt_working_folder)
            elif self.options.get("source").startswith("file://"):
                downloader = LocalGitHandler(
                    uri_or_path=self.options.get("source"),
                    branch=self.options.get("branch", "master"),
                )
                downloader.download(local_path=self.qdt_working_folder)
            else:
                logger.error(
                    f"Source type not implemented yet: {self.options.get('source')}"
                )
                raise NotImplementedError
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
        self.sync_installed_profiles_from_downloaded_profiles(
            downloaded_profiles=profiles_folders
        )

        logger.debug(f"Job {self.ID} ran successfully.")

    def compare_downloaded_with_installed_profiles(
        self, li_downloaded_profiles: Iterable[QdtProfile]
    ) -> tuple[list[QdtProfile], list[QdtProfile], list[QdtProfile]]:
        """Compare versions between downloaded (in QDT working folder) and installed
            (in QGIS) profiles.

        Args:
            li_downloaded_profiles (Iterable[QdtProfile]): downloaded profiles.

        Returns:
            tuple[list[QdtProfile], list[QdtProfile], list[QdtProfile]]: a tuple with
            the following structure (
                list of installed profiles which are outdated (lesser version number),
                list of installed profiles with a different version (lesser or greater),
                list of profiles with the same version number in downloaded/installed
                )
        """
        li_profiles_outdated = []
        li_profiles_different = []
        li_profiles_equal = []

        for downloaded_profile in li_downloaded_profiles:
            if (
                not downloaded_profile.version
                or not downloaded_profile.is_loaded_from_json
            ):
                logger.error(
                    "Unable to load profile.json from downloaded profile "
                    f"{downloaded_profile}, so it's impossible to compare "
                    "versions."
                )
                continue

            if Path(downloaded_profile.path_in_qgis, "profile.json").is_file():
                profile_installed: QdtProfile = QdtProfile.from_json(
                    profile_json_path=Path(
                        downloaded_profile.path_in_qgis, "profile.json"
                    ),
                    profile_folder=downloaded_profile.path_in_qgis,
                )
            else:
                logger.error(
                    "Unable to load profile.json from installed profile "
                    f"{downloaded_profile.path_in_qgis}, so it's impossible to compare "
                    "versions."
                )
                profile_installed: QdtProfile = QdtProfile(
                    folder=downloaded_profile.path_in_qgis, version="0.0.0"
                )

            # compare
            if profile_installed.is_older_than(downloaded_profile):
                li_profiles_outdated.append(downloaded_profile)
            elif profile_installed.version != downloaded_profile.version:
                li_profiles_different.append(downloaded_profile)
            elif profile_installed.version == downloaded_profile.version:
                li_profiles_equal.append(downloaded_profile)
            else:
                continue

        return li_profiles_outdated, li_profiles_different, li_profiles_equal

    def sync_installed_profiles_from_downloaded_profiles(
        self, downloaded_profiles: tuple[QdtProfile]
    ) -> None:
        """Copy downloaded profiles to QGIS profiles folder. If the QGIS profiles folder
            doesn't exist, it will be created and every downloaded profile will be
            copied. If a profile is already installed, it won't be overwritten.

        Args:
            downloaded_profiles (tuple[QdtProfile]): list of downloaded profiles objects
        """
        logger.debug(f"Sync mode: {self.options.get('sync_mode')}.")
        # if local profiles folder exists or it's empty -> copy downloaded profiles
        if not self.qgis_profiles_path.exists() or not any(
            self.qgis_profiles_path.iterdir()
        ):
            logger.info(
                "The QGIS profiles folder does not exist or is empty: "
                f"{self.qgis_profiles_path.resolve()}. Probably a fresh install. "
                "Copying downloaded profiles..."
            )

            # copy all downloaded profiles
            self.sync_overwrite_local_profiles(profiles_to_copy=downloaded_profiles)

        elif self.options.get("sync_mode") == "only_missing":
            already_installed = []
            not_installed = []
            for dl_profile in downloaded_profiles:
                if not dl_profile.path_in_qgis.is_dir() or not any(
                    dl_profile.path_in_qgis.iterdir()
                ):
                    not_installed.append(dl_profile)
                else:
                    already_installed.append(dl_profile)

            if not len(not_installed):
                logger.info(
                    f"Each of the {len(downloaded_profiles)} downloaded plugins are "
                    "already installed."
                )
                compare_for_info = self.compare_downloaded_with_installed_profiles(
                    li_downloaded_profiles=downloaded_profiles
                )
                if len(compare_for_info[0]):
                    logger.info(
                        f"{compare_for_info[0]} of installed plugins are outdated comparing with"
                        f" downloaded ones: {','.join([p.name for p in compare_for_info[0]])}."
                    )
                elif len(compare_for_info[1]):
                    logger.info(
                        f"{compare_for_info[1]} of installed plugins are outdated comparing with"
                        f" downloaded ones: {','.join([p.name for p in compare_for_info[1]])}."
                    )
                else:
                    logger.info("Everything is up-to-date. Nothing to do!")
                return

            info_msg = (
                f"Mixed case. {len(not_installed)} are not installed: "
                f"{','.join([p.name for p in not_installed])}."
            )
            if len(already_installed):
                info_msg += (
                    f" {len(already_installed)} are already installed: "
                    f"{','.join([p.name for p in already_installed])}."
                )

            logger.info(info_msg)

            self.sync_overwrite_local_profiles(profiles_to_copy=not_installed)

        elif self.options.get("sync_mode") == "only_new_version":
            outdated = self.compare_downloaded_with_installed_profiles(
                li_downloaded_profiles=downloaded_profiles
            )[0]
            if not outdated:
                logger.info(
                    "All installed profiles are up-to-date with downloaded ones."
                )
                return
            self.sync_overwrite_local_profiles(profiles_to_copy=outdated)
        elif self.options.get("sync_mode") == "only_different_version":
            outdated, different, same = self.compare_downloaded_with_installed_profiles(
                li_downloaded_profiles=downloaded_profiles
            )
            if not different and not outdated:
                logger.info(
                    f"All installed profiles are the same as downloaded ones: {len(same)}"
                )
                return
            self.sync_overwrite_local_profiles(profiles_to_copy=different + outdated)
        elif self.options.get("sync_mode") == "overwrite":
            logger.debug(
                "Installed profiles are going to be overridden by downloaded ones."
            )
            # copy all downloaded profiles
            self.sync_overwrite_local_profiles(profiles_to_copy=downloaded_profiles)

        else:
            logger.debug(
                "QGIS Profiles folder already exists, it's not empty: "
                f"{self.qgis_profiles_path.resolve()}"
            )

    def sync_copy_only_missing(self, profiles_folder_to_copy: tuple[Path]) -> None:
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
        self, profiles_to_copy: tuple[QdtProfile]
    ) -> None:
        """Overwrite local profiles with downloaded ones.

        Args:
            profiles_to_copy (tuple[QdtProfile]): tuple of profiles to copy
        """

        # copy downloaded profiles into this
        for d in profiles_to_copy:
            logger.info(f"Copying {d.folder} to {d.path_in_qgis}")
            d.path_in_qgis.mkdir(parents=True, exist_ok=True)
            copytree(
                d.folder,
                d.path_in_qgis,
                copy_function=copy2,
                dirs_exist_ok=True,
            )


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
