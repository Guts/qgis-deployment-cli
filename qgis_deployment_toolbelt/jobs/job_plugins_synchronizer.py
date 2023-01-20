#! python3  # noqa: E265

"""
    Synchronize plugins between downloaded and installed profiles.

    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from pathlib import Path
from shutil import unpack_archive
from sys import platform as opersys
from typing import List, Tuple

# package
from qgis_deployment_toolbelt.constants import OS_CONFIG, get_qdt_working_directory
from qgis_deployment_toolbelt.plugins.plugin import QgisPlugin
from qgis_deployment_toolbelt.profiles.qdt_profile import QdtProfile

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################


class JobPluginsSynchronizer:
    """
    Job to download and synchronize plugins.
    """

    ID: str = "qplugins-synchronizer"
    OPTIONS_SCHEMA: dict = {
        "action": {
            "type": str,
            "required": False,
            "default": "create_or_restore",
            "possible_values": ("create", "create_or_restore", "remove"),
            "condition": "in",
        },
        "source": {
            "type": str,
            "required": False,
            "default": None,
            "possible_values": None,
            "condition": None,
        },
    }

    def __init__(self, options: dict) -> None:
        """Instantiate the class.

        :param dict options:  job options.
        """
        self.options: dict = self.validate_options(options)

        # local QDT folder
        self.qdt_working_folder = get_qdt_working_directory()
        logger.debug(f"Working folder: {self.qdt_working_folder}")

        # where QDT downloads plugins
        self.qdt_plugins_folder = self.qdt_working_folder.parent / "plugins"
        self.qdt_plugins_folder.mkdir(exist_ok=True, parents=True)
        logger.info(f"QDT plugins folder: {self.qdt_plugins_folder}")

        # destination profiles folder
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

    def run(self) -> None:
        """Execute job logic."""

        profile_plugins_to_create: List[Tuple[QdtProfile, QgisPlugin, Path]] = []
        profile_plugins_to_restore = []
        profile_plugins_to_upgrade = []

        # parse installed profiles
        profiles_counter = 0
        for profile_json in self.qgis_profiles_path.glob("**/*/profile.json"):
            profiles_counter += 1
            qdt_profile: QdtProfile = QdtProfile.from_json(
                profile_json_path=profile_json,
                profile_folder=profile_json.parent,
            )

            profile_plugins_folder = profile_json.parent / "python/plugins"
            for expected_plugin in qdt_profile.plugins:
                # expected_plugin = expected version to be installed into the profile

                # is the plugin downloaded
                plugin_downloaded_zip_source = (
                    self.qdt_plugins_folder / f"{expected_plugin.id_with_version}.zip"
                )
                if not plugin_downloaded_zip_source.is_file():
                    logger.warning(
                        f"Profile {qdt_profile.name} - "
                        f"Plugin {expected_plugin.name} version "
                        f"{expected_plugin.version} should be installed but its "
                        f"archive is not found: {plugin_downloaded_zip_source}"
                    )
                    continue

                # check if the plugin is already installed or not
                plugin_installed_folder = Path(
                    profile_plugins_folder, expected_plugin.installation_folder_name
                )
                if not plugin_installed_folder.is_dir():
                    logger.debug(
                        f"Plugin {expected_plugin.name} is not present in {qdt_profile.name}. "
                        "It will be added."
                    )
                    profile_plugins_to_create.append(
                        (
                            qdt_profile,
                            expected_plugin,
                            plugin_downloaded_zip_source,
                        )
                    )
                    continue

                # if the plugin is already present into the profile
                plugin_installed = QgisPlugin.from_plugin_folder(
                    input_plugin_folder=plugin_installed_folder
                )

                # print(plugin_installed.version, expected_plugin.version)

                # profile_plugins_to_create.append(
                #     (
                #         qdt_profile,
                #         plugin,
                #         Path(profile_json.parent, "python/plugins", plugin.name),
                #     )
                # )

        # log parse results
        if not any(
            (
                profile_plugins_to_create,
                profile_plugins_to_restore,
                profile_plugins_to_upgrade,
            )
        ):
            logger.info(
                "Every plugins are up to date in the "
                f"{profiles_counter} profiles parsed."
            )
        else:
            self.install_plugin_into_profile(profile_plugins_to_create)

        logger.debug(f"Job {self.ID} ran successfully.")

    def install_plugin_into_profile(
        self, list_plugins_to_profiles: List[Tuple[QdtProfile, QgisPlugin, Path]]
    ):
        """Unzip downloaded plugins into the matching profiles.

        Args:
            list_plugins_to_profiles (List[Tuple[QdtProfile, QgisPlugin, Path]]): list \
                of tuples containing the target profile, the plugin object and the ZIP path.
        """
        for profile, plugin, source_path in list_plugins_to_profiles:
            profile_plugins_folder = profile.folder / "python/plugins"
            profile_plugins_folder.mkdir(parents=True, exist_ok=True)

            unpack_archive(filename=source_path, extract_dir=profile_plugins_folder)

            logger.info(
                f"Profile {profile.name} - "
                f"Plugin {plugin.name} {plugin.version} has been added."
            )

    # -- INTERNAL LOGIC ------------------------------------------------------
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
