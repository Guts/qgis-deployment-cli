#! python3  # noqa: E265

"""
    Handle remote HTTP repository.

    Author: Julien Moura (https://github.com/guts).
"""


# #############################################################################
# ########## Libraries #############
# ##################################


# Standard library
import logging
from pathlib import Path

# 3rd party
import requests

# project
from qgis_deployment_toolbelt.profiles.profiles_handler_base import (
    RemoteProfilesHandlerBase,
)
from qgis_deployment_toolbelt.utils.proxies import get_proxy_settings

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################
class HttpHandler(RemoteProfilesHandlerBase):
    """Handle remote HTTP repositories without git protocol.

    It's designed to handle thoses cases:

    - the distant repository (source) is on a webserver accessible through HTTP protocol
    - the local repository (destination) is on a local network or drive
    """

    def __init__(
        self,
        source_repository_path_or_uri: str,
        source_repository_type: str = "http",
    ) -> None:
        """Constructor.

        Args:
            source_repository_path_or_uri (str | Path): path to the source repository
        """
        self.SOURCE_REPOSITORY_PATH_OR_URL = source_repository_path_or_uri
        super().__init__(source_repository_type=source_repository_type)

        self.SOURCE_REPOSITORY_PATH_OR_URL = source_repository_path_or_uri

        # make sure that URL has a trailing slash
        if isinstance(
            self.SOURCE_REPOSITORY_PATH_OR_URL, str
        ) and not self.SOURCE_REPOSITORY_PATH_OR_URL.endswith("/"):
            self.SOURCE_REPOSITORY_PATH_OR_URL += "/"

    def download(self, destination_local_path: Path):
        """Generic wrapper around the specific logic of this handler.

        Args:
            destination_local_path (Path): path to the local folder where to download

        """
        logger.info(
            f"Start downloading from {self.SOURCE_REPOSITORY_PATH_OR_URL} to "
            f"{destination_local_path}"
        )

        # get qdt-files.json
        req = requests.get(
            url=f"{self.SOURCE_REPOSITORY_PATH_OR_URL}/qdt-files.json",
            proxies=get_proxy_settings(),
        )
        req.raise_for_status()
        data = req.json()

        # make sure destination path exists
        if not destination_local_path.exists():
            logger.debug(
                f"Destination folder ({destination_local_path}) does not exist. "
                "Let's create it!"
            )
            destination_local_path.mkdir(parents=True)

        self.recreate_local_structure(contents=data, parent_path=destination_local_path)

    def recreate_local_structure(self, contents: list, parent_path: Path):
        """
        Crée une structure de dossiers et télécharge des fichiers basée sur la structure JSON.

        :param contents: Liste de dictionnaires représentant les fichiers et dossiers.
        :param parent_path: Chemin du dossier parent dans lequel la structure sera créée.
        """
        for item in contents:
            if item["type"] == "directory":
                logger.debug(
                    f"Folder detected: {item}. Creating local folder: {parent_path.joinpath(item.get('name'))}"
                )
                if item.get("name") == ".":
                    dir_path = parent_path
                else:
                    dir_path = parent_path.joinpath(item.get("name"))
                    dir_path.mkdir(parents=True, exist_ok=True)

                self.recreate_local_structure(
                    contents=item.get("contents"), parent_path=dir_path
                )
            elif item["type"] == "file":
                file_path = parent_path.joinpath(item.get("name"))
                logger.debug(
                    f"File detected. Downloading remote file {item.get('name')} to  local folder: {parent_path.joinpath(item.get('name'))}"
                )
                file_url = f"{self.SOURCE_REPOSITORY_PATH_OR_URL}{file_path}"

                with requests.get(
                    url=file_url, stream=True, proxies=get_proxy_settings()
                ) as response:
                    with file_path.open(mode="wb") as file:
                        for chunk in response.iter_content(chunk_size=10 * 1024):
                            file.write(chunk)


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
