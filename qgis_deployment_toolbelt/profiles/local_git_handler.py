#! python3  # noqa: E265

"""
    Handle local git repository.

    Author: Julien Moura (https://github.com/guts).

    Inspired from: QGIS Resource Sharing
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from pathlib import Path

# 3rd party
from dulwich.errors import NotGitRepository

# project
from qgis_deployment_toolbelt.profiles.git_handler_base import GitHandlerBase

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################
class LocalGitHandler(GitHandlerBase):
    """Handle local git repository."""

    def __init__(
        self, remote_git_uri_or_path: str | Path, branch: str | None = None
    ) -> None:
        """Constructor.

        Args:
            remote_git_uri_or_path (Union[str, Path]): input URI (file://...) or path (S://)
            branch (str, optional): default branch name. Defaults to None.

        Raises:
            NotGitRepository: if uri_or_path doesn't point to a valid Git repository
        """
        self.distant_git_repository_type = "local"

        # clean up
        if remote_git_uri_or_path.startswith("file://"):
            remote_git_uri_or_path = remote_git_uri_or_path[7:]
            logger.debug(
                f"URI cleaning: 'file://' protocol prefix removed. Result: {remote_git_uri_or_path}"
            )
        if remote_git_uri_or_path.endswith(".git"):
            logger.debug(
                f"URI cleaning: '.git' suffix removed. Result: {remote_git_uri_or_path}"
            )
            remote_git_uri_or_path = remote_git_uri_or_path[:-4]

        # validation
        if not self.is_local_path_git_repository(remote_git_uri_or_path):
            raise NotGitRepository(
                f"{remote_git_uri_or_path} is not a valid Git repository."
            )

        self.distant_git_repository_path_or_url = remote_git_uri_or_path
        self.distant_git_repository_branch = branch


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
