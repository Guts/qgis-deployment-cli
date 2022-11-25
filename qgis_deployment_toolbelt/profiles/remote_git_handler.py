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
from shutil import rmtree
from typing import Union

# 3rd party
from dulwich import porcelain
from dulwich.errors import GitProtocolError
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

    def __init__(self, url: str, branch: str = None) -> None:
        """Constructor."""
        # validation
        if not git_validate(url):
            raise ValueError(f"Invalid git URL: {url}")
        self.url = url
        self.branch = branch or self.url_parsed.branch

    @property
    def is_url_git_repository(self) -> bool:
        """Flag if a repository is a git repository.

        :return bool: True if the URL is a valid remote git repository.
        """
        return git_validate(self.url)

    @property
    def url_parsed(self) -> GitUrlParsed:
        """Return URL parsed to extract git information.

        :return GitUrlParsed: parsed URL object
        """
        return git_parse(self.url)

    def download(self, local_path: Union[str, Path]) -> Repo:
        """Generic wrapper around the specific logic of this handler.

        :param Union[str, Path] local_path: path to the local folder where to download
        :return Repo: the local repository object
        """
        return self.clone_or_pull(local_path)

    def is_local_path_git_repository(self, local_path: Union[str, Path]) -> bool:
        """Flag if local folder is a git repository."""
        return Path(local_path / ".git").is_dir()

    def clone_or_pull(self, local_path: Union[str, Path]) -> Repo:
        """Clone or pull remote repository to local path. If this one doesn't exist,
        it's created. If fetch or pull action fail, it removes the existing folder and
        clone the remote again.

        :param Union[str, Path] local_path: path to the folder where to clone (or pull)

        :return Repo: the local repository object
        """
        # convert to path
        if isinstance(local_path, str):
            local_path = Path(local_path)

        # clone
        if local_path.exists() and not self.is_local_path_git_repository(local_path):
            try:
                return self._clone(local_path=local_path)
            except Exception as err:
                logger.error(
                    f"Error cloning the remote repository {self.url} "
                    f"(branch {self.branch}) to {local_path}. "
                    f"Trace: {err}."
                )
                raise err
        elif local_path.exists() and self.is_local_path_git_repository(local_path):
            # FETCH
            try:
                self._fetch(local_path=local_path)
            except GitProtocolError as error:
                logger.error(
                    f"Error fetching {self.url} repository to "
                    f"{local_path.resolve()}. Trace: {error}."
                    "Trying to remove the local folder and cloning again..."
                )
                rmtree(path=local_path, ignore_errors=True)
                return self.clone_or_pull(local_path=local_path)
            # PULL
            try:
                return self._pull(local_path=local_path)
            except GitProtocolError as error:
                logger.error(
                    f"Error fetching {self.url} repository to "
                    f"{local_path.resolve()}. Trace: {error}."
                    "Trying to remove the local folder and cloning again..."
                )
                rmtree(path=local_path, ignore_errors=True)
                return self.clone_or_pull(local_path=local_path)
        elif not local_path.exists():
            logger.debug(
                f"Local path does not exists: {local_path.as_uri()}. "
                "Creating it and trying again..."
            )
            local_path.mkdir(parents=True, exist_ok=True)
            return self.clone_or_pull(local_path)

    def _clone(self, local_path: Union[str, Path]) -> Repo:
        """Clone the remote repository to local path.

        :param Union[str, Path] local_path: path to the folder where to clone

        :return Repo: the local repository object
        """

        # clone
        if local_path.exists() and not self.is_local_path_git_repository(local_path):
            logger.info(f"Cloning repository {self.url} to {local_path}")
            local_repo = porcelain.clone(
                source=self.url,
                target=str(local_path.resolve()),
                branch=self.branch,
                depth=5,
            )
            gobj = local_repo.get_object(local_repo.head())
            logger.debug(
                f"Latest commit cloned: {gobj.sha().hexdigest()} by {gobj.author}"
                f" at {gobj.commit_time}"
            )
            return local_repo

    def _fetch(self, local_path: Union[str, Path]) -> Repo:
        """Fetch the remote repository from the existing local repository.

        :param Union[str, Path] local_path: path to the folder where to fetch

        :return Repo: the local repository object
        """
        with porcelain.open_repo_closing(str(local_path.resolve())) as local_repo:
            logger.info(
                f"Fetching repository {self.url} to {local_path}",
            )
            porcelain.fetch(
                repo=local_repo,
                remote_location=self.url,
                force=True,
                prune=True,
                depth=5,
            )

    def _pull(self, local_path: Union[str, Path]) -> Repo:
        """Pull the remote repository from the existing local repository.

        :param Union[str, Path] local_path: path to the folder where to pull

        :return Repo: the local repository object
        """
        with porcelain.open_repo_closing(str(local_path.resolve())) as local_repo:
            logger.info(f"Pulling repository {self.url} to {local_path}")
            porcelain.pull(repo=local_repo, remote_location=self.url, force=True)
            gobj = local_repo.get_object(local_repo.head())
            logger.debug(
                f"Latest commit cloned: {gobj.sha().hexdigest()} by {gobj.author}"
                f" at {gobj.commit_time}"
            )
        return local_repo


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
