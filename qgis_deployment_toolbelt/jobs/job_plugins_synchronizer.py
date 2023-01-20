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
from sys import platform as opersys

# package
from qgis_deployment_toolbelt.constants import OS_CONFIG, get_qdt_working_directory
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
        # parse downloaded profiles
        for profile_json in self.qgis_profiles_path.glob("**/*/profile.json"):
            qdt_profile: QdtProfile = QdtProfile.from_json(
                profile_json_path=profile_json,
                profile_folder=profile_json.parent,
            )

            profile_plugins_to_install = []
            for plugin in qdt_profile.plugins:
                # plugin = expected version to be installed into the profile

                # is the plugin downloaded
                plugin_downloaded_zip_source = (
                    self.qdt_plugins_folder / f"{plugin.id_with_version}.zip"
                )
                if not plugin_downloaded_zip_source.is_file():
                    logger.warning(
                        f"Profile {qdt_profile.name} - "
                        f"Plugin {plugin.name} version {plugin.version} should be "
                        "installed but its downloaded archive is not found: "
                        f"{plugin_downloaded_zip_source}"
                    )
                    continue

                profile_plugins_to_install.append(
                    (
                        qdt_profile,
                        plugin,
                        Path(profile_json.parent, "python/plugins", plugin.name),
                    )
                )

        logger.debug(f"Job {self.ID} ran successfully.")

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
