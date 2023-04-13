#! python3  # noqa: E265

"""
    Download plugins listed into profiles.

    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from sys import platform as opersys

# package
from qgis_deployment_toolbelt.__about__ import __title_clean__
from qgis_deployment_toolbelt.constants import OS_CONFIG, get_qdt_working_directory
from qgis_deployment_toolbelt.jobs.generic_job import GenericJob
from qgis_deployment_toolbelt.plugins.plugin import QgisPlugin
from qgis_deployment_toolbelt.profiles.qdt_profile import QdtProfile
from qgis_deployment_toolbelt.utils.file_downloader import download_remote_file_to_local

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################


class JobPluginsDownloader(GenericJob):
    """
    Job to download plugins.
    """

    ID: str = "qplugins-downloader"
    OPTIONS_SCHEMA: dict = {
        "force": {
            "type": bool,
            "required": False,
            "default": False,
            "possible_values": None,
            "condition": None,
        },
        "threads": {
            "type": int,
            "required": False,
            "default": 5,
            "possible_values": (1, 2, 3, 4, 5),
            "condition": "in",
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

        # filter plugins to download, filtering out those which are not already present locally
        if self.options.get("force") is True:
            qdt_plugins_to_download = qdt_referenced_plugins
        else:
            qdt_plugins_to_download = self.filter_list_downloadable_plugins(
                input_list=qdt_referenced_plugins
            )
            if not len(qdt_plugins_to_download):
                logger.info(
                    f"All referenced plugins are already present in {self.qdt_plugins_folder}. "
                    "Skipping download step."
                )
                return

        # launch download
        downloaded_plugins, failed_downloads = self.download_plugins(
            plugins_to_download=qdt_plugins_to_download,
            destination_parent_folder=self.qdt_plugins_folder,
            threads=self.options.get("threads", 5),
        )
        logger.debug(f"{len(downloaded_plugins)} plugins downloaded.")
        if len(failed_downloads):
            logger.error(
                f"{len(failed_downloads)} failed plugin downloads. "
                "Check previous log lines."
            )

        logger.debug(f"Job {self.ID} ran successfully.")

    def download_plugins(
        self,
        plugins_to_download: list[QgisPlugin],
        destination_parent_folder: Path,
        threads: int = 5,
    ) -> tuple[list[Path], list[Path]]:
        """Download listed plugins into the specified folder, using multithreads or not.

        Args:
            plugins_to_download (List[QgisPlugin]): list of plugins to download
            destination_parent_folder (Path): where to store downloaded plugins
            threads (int, optional): number of threads to use. If 0, downloads will be \
                performed synchronously. Defaults to 5.

        Returns:
            Tuple[List[Path],List[Path]]: tuple of (downloaded plugins, failed downloads)
        """
        downloaded_plugins: list[QgisPlugin] = []
        failed_plugins: list[QgisPlugin] = []

        if threads < 2:
            logger.debug(f"Downloading {len(plugins_to_download)} threads.")
            for plugin in plugins_to_download:
                # local path
                plugin_download_path = Path(
                    destination_parent_folder, f"{plugin.id_with_version}.zip"
                )
                try:
                    download_remote_file_to_local(
                        local_file_path=plugin_download_path,
                        remote_url_to_download=plugin.download_url,
                        content_type="application/zip",
                    )
                    logger.info(
                        f"Plugin {plugin.name} from {plugin.guess_download_url} "
                        f"downloaded in {plugin_download_path}"
                    )
                    downloaded_plugins.append(plugin)
                except Exception as err:
                    logger.error(
                        f"Download of plugin {plugin.name} failed. Trace: {err}"
                    )
                    failed_plugins.append(plugin)
                    continue
        else:
            logger.debug(
                f"Downloading {len(plugins_to_download)} using {threads} simultaneously."
            )
            with ThreadPoolExecutor(
                max_workers=threads, thread_name_prefix=f"{__title_clean__}"
            ) as executor:
                for plugin in plugins_to_download:
                    # local path
                    plugin_download_path = Path(
                        destination_parent_folder, f"{plugin.id_with_version}.zip"
                    )

                    # submit download to pool
                    try:
                        executor.submit(
                            # func to execute
                            download_remote_file_to_local,
                            # func parameters
                            local_file_path=plugin_download_path,
                            remote_url_to_download=plugin.download_url,
                            content_type="application/zip",
                        )
                        downloaded_plugins.append(plugin)
                    except Exception as err:
                        logger.error(err)
                        failed_plugins.append(plugin)

        return downloaded_plugins, failed_plugins

    def list_referenced_plugins(self, parent_folder: Path) -> list[QgisPlugin]:
        """Return a list of plugins referenced in profile.json files found within a \
            parent folder and sorted by unique id with version.

        Args:
            parent_folder (Path): folder to start searching for profile.json files

        Returns:
            List[QgisPlugin]: list of plugins referenced within profile.json files
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
            input_list (List[QgisPlugin]): list of plugins to filter

        Returns:
            List[QgisPlugin]: list of plugins to download
        """
        plugins_to_download = []

        for plugin in input_list:
            # keep only if remote
            if plugin.location != "remote":
                logger.debug(
                    f"Ignoring plugin '{plugin.name}' because it's not stored remotly."
                )
                continue

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


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
