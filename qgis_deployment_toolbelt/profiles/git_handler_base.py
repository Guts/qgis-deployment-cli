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
from typing import Literal

# 3rd party
from dulwich import porcelain
from dulwich.errors import GitProtocolError, NotGitRepository
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
class GitHandlerBase:
    """Common git repository handler using dulwich.

    It's designed to handle thoses cases:

    - the distant repository is on a local network or drive
    - the distant repository is on Internet (github.com, gitlab.com, gitlab.company.org...)
    - the local repository is on a local network or drive
    """

    distant_git_repository_path_or_url: Path | str | None = None
    distant_git_repository_type: Literal["local", "remote"] | None = None
    distant_git_repository_branch: str | None = None

    local_git_repository_path: Path | None = None
    local_git_repository_active_branch: str | None = None

    def url_parsed(self, remote_git_url: str) -> GitUrlParsed:
        """Return URL parsed to extract git information.

        Returns:
            GitUrlParsed: parsed URL object
        """
        return git_parse(remote_git_url)

    def is_local_path_git_repository(self, local_path: Path) -> bool:
        """Flag if local folder is a git repository.

        Args:
            local_path (Path): path to check

        Returns:
            bool: True if there is a .git subfolder
        """
        try:
            Repo(root=f"{local_path.resolve()}")
            return True
        except NotGitRepository as err:
            logger.error(f"{local_path} is not a valid Git repository. Trace: {err}")
            return False
        except Exception as err:
            logger.error(
                f"Something went wrong when checking if {local_path} is a valid "
                f"Git repository. Trace: {err}"
            )
            return False

    def is_url_git_repository(self, remote_git_url: str) -> bool:
        """Flag if the remote URL is a git repository.

        Args:
            remote_git_url (str): URL pointing to a remote git repository.

        Returns:
            bool: True if the URL is a valid git repository.
        """
        return git_validate(remote_git_url)

    def download(self, local_path: str | Path) -> Repo:
        """Generic wrapper around the specific logic of this handler.

        Args:
            local_path (str | Path): path to the local folder where to download

        Returns:
            Repo: the local repository object
        """
        local_git_repository = self.clone_or_pull(local_path)
        if isinstance(local_git_repository, Repo):
            self.local_git_repository_active_branch = porcelain.active_branch(
                local_git_repository
            )
        return local_git_repository

    def clone_or_pull(self, local_path: str | Path) -> Repo:
        """Clone or pull remote repository to local path. If this one doesn't exist,
        it's created. If fetch or pull action fail, it removes the existing folder and
        clone the remote again.

        Args:
            local_path (str | Path): path to the folder where to clone (or pull)

        Raises:
            err: if something fails during clone or pull operations

        Returns:
            Repo: the local repository object
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
                    f"Error cloning the remote repository {self.distant_git_repository_path_or_url} "
                    f"(branch {self.distant_git_repository_branch}) to {local_path}. "
                    f"Trace: {err}."
                )
                raise err
        elif local_path.exists() and self.is_local_path_git_repository(local_path):
            # FETCH
            try:
                self._fetch(local_path=local_path)
            except GitProtocolError as error:
                logger.error(
                    f"Error fetching {self.distant_git_repository_path_or_url} "
                    f"repository to {local_path.resolve()}. Trace: {error}."
                    "Trying to remove the local folder and cloning again..."
                )
                rmtree(path=local_path, ignore_errors=True)
                return self.clone_or_pull(local_path=local_path)
            # PULL
            try:
                return self._pull(local_path=local_path)
            except GitProtocolError as error:
                logger.error(
                    f"Error pulling {self.distant_git_repository_path_or_url} "
                    f"repository to {local_path.resolve()}. Trace: {error}."
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
            return self.clone_or_pull(local_path=local_path)

    def _clone(self, local_path: Path) -> Repo:
        """Clone the remote repository to local path.

        Args:
            local_path (Path): path to the folder where to clone

        Returns:
            Repo: the local repository object
        """
        # clone
        logger.info(
            f"Cloning repository {self.distant_git_repository_path_or_url} to {local_path}"
        )
        local_repo = porcelain.clone(
            source=self.distant_git_repository_path_or_url,
            target=f"{local_path.resolve()}",
            branch=self.distant_git_repository_branch,
            depth=0,
        )
        gobj = local_repo.get_object(local_repo.head())
        logger.debug(
            f"Active branch: {porcelain.active_branch(local_repo)}. "
            f"Latest commit cloned: {gobj.sha().hexdigest()} by {gobj.author}"
            f" at {gobj.commit_time}."
        )
        return local_repo

    def _fetch(self, local_path: Path) -> Repo:
        """Fetch the remote repository from the existing local repository.

        Args:
            local_path (Path): path to the folder where to fetch

        Returns:
            Repo: the local repository object
        """
        # with porcelain.open_repo_closing(str(local_path.resolve())) as local_repo:
        logger.info(
            f"Fetching repository {self.distant_git_repository_path_or_url} to {local_path}",
        )
        local_repo = Repo(root=f"{local_path.resolve()}")
        porcelain.fetch(
            repo=f"{local_path.resolve()}",
            remote_location=self.distant_git_repository_path_or_url,
            force=True,
            prune=True,
            prune_tags=True,
            depth=0,
        )
        logger.debug(
            f"Repository {local_path.resolve()} has been fetched from "
            f"remote {self.distant_git_repository_path_or_url}. "
            f"Local active branch: {porcelain.active_branch(local_repo)}."
        )

    def _pull(self, local_path: Path) -> Repo:
        """Pull the remote repository from the existing local repository.

        Args:
            local_path (Path): path to the folder where to pull

        Returns:
            Repo: the local repository object
        """
        local_repo = Repo(root=f"{local_path.resolve()}")
        logger.info(
            f"Pulling repository {self.distant_git_repository_path_or_url} to {local_path}"
        )
        porcelain.pull(
            repo=local_path,
            remote_location=self.distant_git_repository_path_or_url,
            force=True,
        )
        gobj = local_repo.get_object(local_repo.head())
        logger.debug(
            f"Repository {local_path.resolve()} has been pulled. "
            f"Local active branch: {porcelain.active_branch(local_repo)}. "
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
