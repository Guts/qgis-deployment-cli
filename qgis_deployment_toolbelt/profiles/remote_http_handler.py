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
        req.json()


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
