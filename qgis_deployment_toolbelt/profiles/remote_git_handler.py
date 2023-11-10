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

# 3rd party
from giturlparse import validate as git_validate

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
class RemoteGitHandler(GitHandlerBase):
    """Handle remote git repository."""

    def __init__(self, remote_git_uri_or_path: str, branch: str | None = None) -> None:
        """Constructor.

        Args:
            remote_git_uri_or_path (Union[str, Path]): input URI (http://, https://, git://)
            branch (str, optional): default branch name. Defaults to None.

        """
        self.distant_git_repository_type = "remote"

        # validation
        if not git_validate(remote_git_uri_or_path):
            raise ValueError(f"Invalid git URL: {remote_git_uri_or_path}")

        self.distant_git_repository_path_or_url = remote_git_uri_or_path

        if isinstance(branch, (str, bytes)):
            self.distant_git_repository_branch = branch
        else:
            self.distant_git_repository_branch = self.url_parsed(
                self.distant_git_repository_path_or_url
            ).branch


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
