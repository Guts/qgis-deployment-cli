#! python3  # noqa: E265

"""
    Handle remote git repository.

    Author: Julien Moura (https://github.com/guts).

    Inspired from: QGIS Resource Sharing
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging

# project
from qgis_deployment_toolbelt.profiles.git_handler_base import GitHandlerBase

# 3rd party


# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################
class RemoteGitHandler(GitHandlerBase):
    """Handle remote git repository."""

    def __init__(
        self,
        source_repository_url: str,
        source_repository_type: str = "remote",
        branch_to_use: str | None = None,
    ) -> None:
        """Constructor.

        Args:
            source_repository_url (Union[str, Path]): input URI (http://, https://, git://)

        """
        super().__init__(
            source_repository_type=source_repository_type, branch_to_use=branch_to_use
        )

        # validation
        self.SOURCE_REPOSITORY_PATH_OR_URL = source_repository_url
        self.is_valid_git_repository()

        if isinstance(branch_to_use, str) and len(branch_to_use):
            self.DESTINATION_BRANCH_TO_USE = branch_to_use


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
