#! python3  # noqa: E265

"""
    Manage plugins listed into profiles.

    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from concurrent.futures import ThreadPoolExecutor
from configparser import ConfigParser
from os import getenv
from pathlib import Path
from sys import platform as opersys

# package
from qgis_deployment_toolbelt.__about__ import __title_clean__
from qgis_deployment_toolbelt.constants import OS_CONFIG, get_qdt_working_directory
from qgis_deployment_toolbelt.plugins.plugin import QgisPlugin
from qgis_deployment_toolbelt.profiles.qdt_profile import QdtProfile
from qgis_deployment_toolbelt.utils.check_path import check_path
from qgis_deployment_toolbelt.utils.file_downloader import download_remote_file_to_local
from qgis_deployment_toolbelt.utils.slugger import sluggy

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################


class JobPluginsManager:
    """
    Job to download and synchronize plugins.
    """

    ID: str = "qplugins-manager"
    OPTIONS_SCHEMA: dict = {
        "action": {
            "type": str,
            "required": False,
            "default": "create_or_restore",
            "possible_values": ("create", "create_or_restore", "remove"),
            "condition": "in",
        }
    }

    def __init__(self, options: dict) -> None:
        """Instantiate the class.

        :param dict options: profiles source (remote, can be a local network) and
        destination (local).
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
        # list plugins through different profiles
        qdt_referenced_plugins = self.list_referenced_plugins(
            parent_folder=self.qdt_working_folder
        )
        if not len(qdt_referenced_plugins):
            logger.info(
                f"No plugin found in profile.json files within {self.qdt_working_folder}"
            )
            return

        # filter plugins to download, filtering out those which are not already  present locally
        qdt_plugins_to_download = self.filter_list_downloadable_plugins(
            input_list=qdt_referenced_plugins
        )
        if not len(qdt_plugins_to_download):
            logger.info(
                f"All referenced plugins are already present in {self.qdt_plugins_folder}. "
                "Skipping download step."
            )
            return

        # download plugins into the QDT local folder - only those which are not already present

        # if self.options.get("action") in ("create", "create_or_restore"):

        #     for plugin in qdt_referenced_plugins:
        #         # destination

        #         with ThreadPoolExecutor(
        #             max_workers=5, thread_name_prefix=f"{__title_clean__}"
        #         ) as executor:
        #             for plugin in qdt_profile.plugins:
        #                 # local path
        #                 qdt_dest_plugin_path = Path(
        #                     self.qdt_plugins_folder,
        #                     sluggy(plugin.name),
        #                     f"{sluggy(plugin.version)}.zip",
        #                 )

        #                 # submit download to pool
        #                 executor.submit(
        #                     # func to execute
        #                     download_remote_file_to_local,
        #                     # func parameters
        #                     local_file_path=qdt_dest_plugin_path,
        #                     remote_url_to_download=plugin.url,
        #                     content_type="application/zip",
        #                 )

        # li_installed_profiles_path = [
        #     d
        #     for d in self.qgis_profiles_path.iterdir()
        #     if d.is_dir() and not d.name.startswith(".")
        # ]

        # if self.options.get("action") in ("create", "create_or_restore"):
        #     for profile_dir in li_installed_profiles_path:

        #         # case where splash image is specified into the profile.json
        #         if Path(profile_dir / "profile.json").is_file():
        #             qdt_profile = QdtProfile.from_json(
        #                 profile_json_path=Path(profile_dir / "profile.json"),
        #                 profile_folder=profile_dir.resolve(),
        #             )
        #             print("hop")
        #             # plugins
        #             # profile_plugins_dir = profile_dir / "python/plugins"

        #             with ThreadPoolExecutor(
        #                 max_workers=5, thread_name_prefix=f"{__title_clean__}"
        #             ) as executor:
        #                 for plugin in qdt_profile.plugins:
        #                     # local path
        #                     qdt_dest_plugin_path = Path(
        #                         self.qdt_plugins_folder,
        #                         sluggy(plugin.name),
        #                         f"{sluggy(plugin.version)}.zip",
        #                     )

        #                     # submit download to pool
        #                     executor.submit(
        #                         # func to execute
        #                         download_remote_file_to_local,
        #                         # func parameters
        #                         local_file_path=qdt_dest_plugin_path,
        #                         remote_url_to_download=plugin.url,
        #                         content_type="application/zip",
        #                     )

        #         else:
        #             logger.debug(f"No profile.json found for profile '{profile_dir}")
        #             continue

        # else:
        #     raise NotImplementedError

        logger.debug(f"Job {self.ID} ran successfully.")

    def list_referenced_plugins(self, parent_folder: Path) -> list[QgisPlugin]:
        """Return a list of plugins referenced in profile.json files found within a \
            parent folder and sorted by unique id with version.

        Args:
            parent_folder (Path): folder to start searching for profile.json files

        Returns:
            list[QgisPlugin]: list of plugins referenced within profile.json files
        """
        unique_profiles_identifiers: list = []
        all_profiles: list[QgisPlugin] = []

        profile_json_counter: int = 0
        for profile_json in parent_folder.glob("**/*/profile.json"):
            # increment counter
            profile_json_counter += 1

            # read profile.json
            qdt_profile = QdtProfile.from_json(
                profile_json_path=profile_json,
                profile_folder=profile_json.parent,
            )

            # parse profile plugins
            for plugin in qdt_profile.plugins:
                if plugin.id_with_version not in unique_profiles_identifiers:
                    unique_profiles_identifiers.append(plugin.id_with_version)
                    all_profiles.append(plugin)

        logger.debug(
            f"{len(unique_profiles_identifiers)} unique plugins referenced in "
            f"{profile_json_counter} profiles.json in {parent_folder.resolve()}: "
            f"{','.join(sorted(unique_profiles_identifiers))}"
        )
        return sorted(all_profiles, key=lambda x: x.id_with_version)

    def filter_list_downloadable_plugins(
        self, input_list: list[QgisPlugin]
    ) -> list[QgisPlugin]:
        """Filter input list of plugins keeping only those which are not present within \
            the local QDT plugins folder.

        Args:
            input_list (list[QgisPlugin]): list of plugins to filter

        Returns:
            list[QgisPlugin]: list of plugins to download
        """
        plugins_to_download = []

        for plugin in input_list:
            # build destination path
            plugin_download_path = Path(
                self.qdt_plugins_folder, f"{plugin.id_with_version}.zip"
            )

            # check if file already exists
            if plugin_download_path.is_file():
                logger.debug(
                    f"Plugin already exists at {plugin_download_path}, so it "
                    "won't be downloaded."
                )
                continue

            plugins_to_download.append(plugin)

        return plugins_to_download

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
