#! python3  # noqa: E265

"""
    Base of QDT jobs.

    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from os import getenv
from pathlib import Path

# package
from qgis_deployment_toolbelt.constants import (
    OSConfiguration,
    get_qdt_working_directory,
)
from qgis_deployment_toolbelt.exceptions import (
    JobOptionBadName,
    JobOptionBadValue,
    JobOptionBadValueType,
)
from qgis_deployment_toolbelt.profiles.qdt_profile import QdtProfile

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)

# #############################################################################
# ########## Classes ###############
# ##################################


class GenericJob:
    """Generic base for QDT jobs."""

    ID: str = ""
    OPTIONS_SCHEMA: dict[dict] = dict(dict())

    def __init__(self) -> None:
        """Object instanciation."""
        # operating system configuration
        self.os_config = OSConfiguration.from_opersys()

        # local QDT folders
        self.qdt_working_folder = get_qdt_working_directory()
        if not self.qdt_working_folder.exists():
            logger.info(
                f"QDT downloaded folder not found: {self.qdt_working_folder}. "
                "Creating it to properly run the job."
            )
            self.qdt_working_folder.mkdir(parents=True, exist_ok=True)
        logger.debug(f"QDT working folder: {self.qdt_working_folder}")

        self.qdt_downloaded_repositories = self.qdt_working_folder.joinpath(
            f"repositories/{getenv('QDT_TMP_RUNNING_SCENARIO_ID', 'default')}"
        )
        self.qdt_plugins_folder = self.qdt_working_folder.joinpath("plugins")

        # destination profiles folder
        self.qgis_profiles_path: Path = self.os_config.qgis_profiles_path
        if not self.qgis_profiles_path.exists():
            logger.info(
                f"Installed QGIS profiles folder not found: {self.qgis_profiles_path}. "
                "Creating it to properly run the job."
            )
            self.qgis_profiles_path.mkdir(parents=True)
        logger.debug(f"Installed QGIS profiles folder: {self.qgis_profiles_path}")

    def list_downloaded_profiles(self) -> tuple[QdtProfile] | None:
        """List downloaded QGIS profiles, i.e. a profile's folder located into the QDT
            working folder.
            Typically: `~/.cache/qgis-deployment-toolbelt/repositories/geotribu` or
            `%USERPROFILE%/.cache/qgis-deployment-toolbelt/repositories/geotribu`).

        Returns:
            tuple[QdtProfile] | None: tuple of profiles objects or None if no profile
                folder listed
        """
        return self.filter_profiles_folder(
            start_parent_folder=self.qdt_downloaded_repositories
        )

    def list_installed_profiles(self) -> tuple[QdtProfile] | None:
        """List installed QGIS profiles, i.e. a profile's folder located into the QGIS
            profiles path and so accessible to the end-user through the QGIS interface.
            Typically: `~/.local/share/QGIS/QGIS3/profiles/geotribu` or
            `%APPDATA%/QGIS/QGIS3/profiles/geotribu`).

        Returns:
            tuple[QdtProfile] | None: tuple of profiles objects or Non if no profile is
                installed in QGIS3/profiles
        """
        return self.filter_profiles_folder(start_parent_folder=self.qgis_profiles_path)

    def filter_profiles_folder(
        self, start_parent_folder: Path
    ) -> tuple[QdtProfile] | None:
        """Parse a folder structure to filter on QGIS profiles folders.

        Returns:
            tuple[QdtProfile] | None: tuple of profiles objects or Non if no profile
                folder found
        """
        # first, try to get folders containing a profile.json
        qgis_profiles_folder = [
            QdtProfile.from_json(profile_json_path=f, profile_folder=f.parent)
            for f in start_parent_folder.glob("**/profile.json")
        ]
        if len(qgis_profiles_folder):
            logger.debug(
                f"{len(qgis_profiles_folder)} profiles found within {start_parent_folder}"
            )
            return tuple(qgis_profiles_folder)

        # if empty, try to identify if a folder is a QGIS profile - but unsure
        for d in start_parent_folder.glob("**"):
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

    def validate_options(self, options: dict[dict]) -> dict[dict]:
        """Validate options.

        Args:
            options (dict[dict]): options to validate.

        Raises:
            ValueError: if option has an invalid name or doesn't comply with condition
            TypeError: if the option does'nt not comply with expected type

        Returns:
            dict[dict]: options if valid
        """
        if not isinstance(options, dict):
            raise TypeError(f"Options to validate must be a dict, not {type(options)}.")

        for option in options:
            if option not in self.OPTIONS_SCHEMA:
                raise JobOptionBadName(
                    job_id=self.ID,
                    bad_option_name=option,
                    expected_options_names=self.OPTIONS_SCHEMA.keys(),
                )

            option_in = options.get(option)
            option_def: dict = self.OPTIONS_SCHEMA.get(option)
            # check value type
            if not isinstance(option_in, option_def.get("type")):
                raise JobOptionBadValueType(
                    job_id=self.ID,
                    bad_option_name=option,
                    bad_option_value=option_in,
                    expected_option_type=option_def.get("type"),
                )
            # check value condition
            if option_def.get("condition") == "startswith" and not option_in.startswith(
                option_def.get("possible_values")
            ):
                raise JobOptionBadValue(
                    job_id=self.ID,
                    bad_option_name=option,
                    bad_option_value=option_in,
                    condition="startswith",
                    accepted_values=option_def.get("possible_values"),
                )
            elif option_def.get(
                "condition"
            ) == "in" and option_in not in option_def.get("possible_values"):
                raise JobOptionBadValue(
                    job_id=self.ID,
                    bad_option_name=option,
                    bad_option_value=option_in,
                    condition="startswith",
                    accepted_values=option_def.get("possible_values"),
                )
            else:
                pass

        return options
