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
from pathlib import Path
from typing import Union

# 3rd party
from dulwich import porcelain
from dulwich.repo import Repo
from giturlparse import GitUrlParsed
from giturlparse import parse as git_parse
from giturlparse import validate as git_validate

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################
class RemoteGitHandler:
    """Handle generic git remote repository."""

    def __init__(self, url: str) -> None:
        """Constructor."""
        # validation
        if not git_validate(url):
            raise ValueError(f"Invalid git URL: {url}")
        self.url = url

    @property
    def is_url_git_repository(self) -> bool:
        """Flag if a repository is a git repository."""
        return git_validate(self.url)

    @property
    def url_parsed(self) -> GitUrlParsed:
        return git_parse(self.url)

    def download(self, local_path: Union[str, Path]) -> Repo:
        """Just a wrapper around the specific logic of this handler.

        :param Union[str, Path] local_path: path to the local folder where to download
        :return Repo: the local repository object
        """
        return self.clone_or_pull(local_path)

    def is_local_path_git_repository(self, local_path: Union[str, Path]) -> bool:
        """Flag if local folder is a git repository."""
        return Path(local_path / ".git").is_dir()

    def clone_or_pull(self, local_path: Union[str, Path]) -> Repo:
        """Clone or pull remote repository to local path.
        If this one doesn't exist, it's created.

        :param Union[str, Path] local_path: path to the folder where to clone (or pull)
        :return Repo: the local repository object
        """
        # convert to path
        if isinstance(local_path, str):
            local_path = Path(local_path)

        # clone
        if local_path.exists() and not self.is_local_path_git_repository(local_path):
            logger.info(f"Cloning repository {self.url} to {local_path}")
            return porcelain.clone(
                source=self.url,
                target=str(local_path.resolve()),
                branch=self.url_parsed.branch,
                depth=5,
            )
        elif local_path.exists() and self.is_local_path_git_repository(local_path):
            logger.info(f"Pulling repository {self.url} to {local_path}")
            porcelain.pull(str(local_path.resolve()), force=True)
            return Repo(root=str(local_path.resolve()))
        elif not local_path.exists():
            logger.debug(
                f"Local path does not exists: {local_path.as_uri()}. "
                "Creating it and trying again..."
            )
            local_path.mkdir(parents=True, exist_ok=True)
            return self.clone_or_pull(local_path)


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
