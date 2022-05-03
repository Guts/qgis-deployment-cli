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
import shutil
import traceback
import warnings
from pathlib import Path
from typing import Union

# 3rd party
from dulwich import porcelain
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
        return git_validate(self._url)

    def is_local_path_git_repository(self, local_path: Union[str, Path]) -> bool:
        """Flag if a repository is a git repository."""
        return git_validate(self._url)

    @property
    def url_parsed(self) -> GitUrlParsed:
        return git_parse(self._url)

    def clone_or_pull(self, local_path: Union[str, Path]) -> None:
        """Clone or pull a repository."""
        # clone
        if not Path(local_path).exists():
            logger.info(f"Cloning repository {self.url} to {local_path}")
            porcelain.clone(self.url, local_path)
        else:
            logger.info(f"Pulling repository {self.url} to {local_path}")
            porcelain.pull(local_path)


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
