#! python3  # noqa: E265

"""
    GeoServer authentication.

    Author: In Geo Veritas (Julien Moura)
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from pathlib import Path

# 3rd party
from lxml import etree

# #############################################################################
# ########## Globals ###############
# ##################################

logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################


class QgisPluginsDownloader:
    """Helper module to download plugins: compare versions, install, reinstall."""

    def __init__(
        self,
        repository_source: str,
        min_qgis_version: str = "3.16",
        max_qgis_version: str = "3.99",
    ):
        """Instanciation method."""
        # store args as attrs
        self.min_qgis_version = min_qgis_version
        self.max_qgis_version = max_qgis_version

        # check type of source
        repository_path = Path(repository_source)
        if repository_path.is_dir():
            self.repository_type = "local_folder"
        elif repository_path.is_file():
            self.repository_type = "local_folder"
        elif str(repository_path).startswith(("//", r"\\")):
            self.repository_type = "local_network"
        elif str(repository_path).startswith(("http", "ftp")):
            self.repository_type = "remote_url"
        else:
            raise ValueError(
                f"Unable to identify the repository type: {repository_path}"
            )

    def is_official_repository(self):
        pass

    def is_latest_version(self):
        pass

    def get_code_repository(self):
        pass


# #############################################################################
# ##### Main #######################
# ##################################
if __name__ == "__main__":
    pass
