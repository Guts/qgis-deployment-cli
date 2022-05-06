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
        # TODO: handle custom profiles folder through QGIS_CUSTOM_CONFIG_PATH

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

        # copy profiles to the QGIS 3
        self.sync_local_profiles()

        logger.debug(f"Job {self.ID} ran successfully.")

    def sync_local_profiles(self) -> None:
        """Sync local profiles."""
        # check if local profiles folder exists or it's empty
        if not self.qgis_profiles_path.exists() or not any(
            self.qgis_profiles_path.iterdir()
        ):
            # ensure it exists
            self.qgis_profiles_path.mkdir(parents=True, exist_ok=True)
            # copy downloaded profiles into this
            copytree(
                self.local_path,
                self.qgis_profiles_path,
                copy_function=copy2,
                dirs_exist_ok=True,
            )
        else:
            logger.error(
                f"QGIS Profiles folder already exists and it's not empty: {self.qgis_profiles_path.resolve()}"
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
                    f"\nExpected: starts with one of: {', '.join(option_def.get('possible_values'))}"
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
