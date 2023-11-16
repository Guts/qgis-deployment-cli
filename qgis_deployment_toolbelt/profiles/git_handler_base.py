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

    - the distant repository (source) is on a local network or drive
    - the distant repository (source) is on Internet (github.com, gitlab.com, gitlab.company.org...)
    - the local repository (destination) is on a local network or drive
    """

    SOURCE_REPOSITORY_ACTIVE_BRANCH: str | None = None
    SOURCE_REPOSITORY_PATH_OR_URL: Path | str | None = None
    SOURCE_REPOSITORY_TYPE: Literal["local", "remote"] | None = None

    DESTINATION_PATH: Path | None = None
    DESTINATION_BRANCH_TO_USE: str | None = None

    def __init__(
        self,
        source_repository_type: Literal["local", "remote"],
        branch_to_use: str | None = None,
    ) -> None:
        """Object instanciation.

        Args:
            source_repository_type (Literal["local", "remote"]): type of source
                repository
            branch_to_use (str | None, optional): branch to clone or checkout. If None,
                the source active branch will be used. Defaults to None.
        """
        self.DESTINATION_BRANCH_TO_USE = branch_to_use
        self.SOURCE_REPOSITORY_TYPE = source_repository_type

    def url_parsed(self, remote_git_url: str) -> GitUrlParsed:
        """Return URL parsed to extract git information.

        Returns:
            GitUrlParsed: parsed URL object
        """
        return git_parse(remote_git_url)

    def is_valid_git_repository(
        self,
        source_repository_path_or_url: Path | str | None = None,
        raise_error: bool = True,
    ) -> bool:
        # if no local git repository passed, try to use URL defined at object level
        if source_repository_path_or_url is None and isinstance(
            self.SOURCE_REPOSITORY_PATH_OR_URL, str
        ):
            source_repository_path_or_url: str = self.SOURCE_REPOSITORY_PATH_OR_URL

        # check if URL or path is pointing to a valid git repository
        valid_source = True
        if self.SOURCE_REPOSITORY_TYPE == "remote" and self._is_url_git_repository(
            remote_git_url=source_repository_path_or_url
        ):
            valid_source = False
        elif (
            self.SOURCE_REPOSITORY_TYPE == "local"
            and not self._is_local_path_git_repository(
                local_path=source_repository_path_or_url
            )
        ):
            valid_source = False

        # log and/or raise
        err_message = f"{source_repository_path_or_url} is not a valid repository."
        if not valid_source and raise_error:
            raise NotGitRepository(
                f"{source_repository_path_or_url} is not a valid repository."
            )
        elif not valid_source:
            logger.error(err_message)
        else:
            logger.debug(
                f"{source_repository_path_or_url} is a valid "
                f"{self.SOURCE_REPOSITORY_TYPE} repository."
            )

        return valid_source

    def _is_local_path_git_repository(
        self, local_path: Path | None, raise_error: bool = False
    ) -> bool:
        """Check if local folder is a git repository.

        Args:
            local_path (Path, optional): path to check
            just_check (bool, optional): if enabled no error message is log but debug.
                Defaults to False.

        Returns:
            bool: True if there is a .git subfolder
        """
        # if no local git repository passed, try to use URL defined at object level
        if local_path is None and isinstance(self.SOURCE_REPOSITORY_PATH_OR_URL, Path):
            local_path: Path = self.SOURCE_REPOSITORY_PATH_OR_URL

        try:
            Repo(root=f"{local_path.resolve()}")
            return True
        except NotGitRepository as err:
            if raise_error:
                logger.debug(f"{local_path} is not a valid Git repository")
                return False
            logger.error(f"{local_path} is not a valid Git repository. Trace: {err}")
            return False
        except Exception as err:
            logger.error(
                f"Something went wrong when checking if {local_path} is a valid "
                f"Git repository. Trace: {err}"
            )
            return False

    def _is_url_git_repository(self, remote_git_url: str | None = None) -> bool:
        """Check if the remote URL is a git repository.

        Args:
            remote_git_url (str): URL pointing to a remote git repository.

        Returns:
            bool: True if the URL is a valid git repository.
        """
        # if remote git URL not passed, try to use URL defined at object level
        if remote_git_url is None and isinstance(
            self.SOURCE_REPOSITORY_PATH_OR_URL, str
        ):
            remote_git_url = self.SOURCE_REPOSITORY_PATH_OR_URL

        return git_validate(remote_git_url)

    def get_active_branch_from_local_repository(
        self, local_git_repository_path: Path | None = None
    ) -> str:
        """Retrieve git active branch from a local repository. Mainly a checker and a
            wrapper around dulwich logic.

        Args:
            local_git_repository_path (Path | None, optional): path to the local
                repository. If not defined, the SOURCE_REPOSITORY_PATH_OR_URL object's
                attribute is used if it exists. Defaults to None.

        Raises:
            NotGitRepository: if the path is not a valid Git Repository

        Returns:
            str: branch name
        """
        # if no local git repository passed, try to use URL defined at object level
        if local_git_repository_path is None and isinstance(
            self.SOURCE_REPOSITORY_PATH_OR_URL, Path
        ):
            local_git_repository_path: Path = self.SOURCE_REPOSITORY_PATH_OR_URL

        if not self._is_local_path_git_repository(local_path=local_git_repository_path):
            raise NotGitRepository(
                f"Unable to determine active branch since {local_git_repository_path} "
                "is not a valid Git repository."
            )

        return porcelain.active_branch(
            repo=Repo(root=f"{local_git_repository_path.resolve()}")
        ).decode()

    def list_remote_branches(
        self, source_repository_path_or_url: Path | str | None = None
    ) -> tuple[str]:
        """Retrieve git active branch from a local repository. Mainly a checker and a
            wrapper around dulwich logic.

        Args:
            source_repository_path_or_url (Path | str, optional): URL or path pointing to a git repository.

        Raises:
            NotGitRepository: if the path is not a valid Git Repository

        Returns:
            tuple[str]: branch name
        """
        # if no local git repository passed, try to use URL defined at object level
        if source_repository_path_or_url is None and isinstance(
            self.SOURCE_REPOSITORY_PATH_OR_URL, str
        ):
            source_repository_path_or_url: str = self.SOURCE_REPOSITORY_PATH_OR_URL

        # check if URL or path is pointing to a valid git repository
        valid_source = True
        if self.SOURCE_REPOSITORY_TYPE == "remote" and self._is_url_git_repository(
            remote_git_url=source_repository_path_or_url
        ):
            valid_source = False
        elif (
            self.SOURCE_REPOSITORY_TYPE == "local"
            and not self._is_local_path_git_repository(
                local_path=source_repository_path_or_url
            )
        ):
            valid_source = False
        if not valid_source:
            raise NotGitRepository(
                f"{source_repository_path_or_url} is not a valid repository."
            )

        ls_remote_refs: dict = porcelain.ls_remote(remote=source_repository_path_or_url)
        if isinstance(ls_remote_refs, dict):
            source_repository_branches: list[str] = [
                ref.decode() for ref in ls_remote_refs if ref.startswith(b"refs/heads/")
            ]
            return tuple(source_repository_branches)
        else:
            return ("",)

    def _is_url_git_repository(self, remote_git_url: str | None = None) -> bool:
        """Flag if the remote URL is a git repository.

        Args:
            remote_git_url (str): URL pointing to a remote git repository.

        Returns:
            bool: True if the URL is a valid git repository.
        """
        # if remote git URL not passed, try to use URL defined at object level
        if remote_git_url is None and isinstance(
            self.SOURCE_REPOSITORY_PATH_OR_URL, str
        ):
            remote_git_url = self.SOURCE_REPOSITORY_PATH_OR_URL

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
            self.SOURCE_REPOSITORY_ACTIVE_BRANCH = porcelain.active_branch(
                local_git_repository
            )
        return local_git_repository

    def clone_or_pull(self, local_path: str | Path, attempt: int = 1) -> Repo:
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
            local_path = Path(local_path).resolve()

        # clone
        if not local_path.exists() and not self._is_local_path_git_repository(
            local_path
        ):
            try:
                return self._clone(local_path=local_path)
            except Exception as err:
                logger.error(
                    f"Error cloning the remote repository {self.SOURCE_REPOSITORY_PATH_OR_URL} "
                    f"(branch {self.SOURCE_REPOSITORY_ACTIVE_BRANCH}) to {local_path}. "
                    f"Trace: {err}."
                )
                if attempt < 2:
                    logger.error(
                        "Clone failed. Removing target folder and trying again."
                    )
                    rmtree(path=local_path, ignore_errors=True)
                    return self.clone_or_pull(local_path=local_path, attempt=2)
                raise err
        elif local_path.exists() and self._is_local_path_git_repository(local_path):
            # FETCH
            try:
                self._fetch(local_path=local_path)
            except GitProtocolError as error:
                logger.error(
                    f"Error fetching {self.SOURCE_REPOSITORY_PATH_OR_URL} "
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
                    f"Error pulling {self.SOURCE_REPOSITORY_PATH_OR_URL} "
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
        logger.debug(
            f"Cloning repository {self.SOURCE_REPOSITORY_PATH_OR_URL} to {local_path}"
        )

        # make sure folder and its parents exist
        if not local_path.exists():
            local_path.mkdir(parents=True, exist_ok=True)

        # make sure branch is bytes
        if isinstance(self.SOURCE_REPOSITORY_ACTIVE_BRANCH, str) and len(
            self.SOURCE_REPOSITORY_ACTIVE_BRANCH
        ):
            branch = self.SOURCE_REPOSITORY_ACTIVE_BRANCH.encode()
        elif isinstance(self.SOURCE_REPOSITORY_ACTIVE_BRANCH, bytes):
            branch = self.SOURCE_REPOSITORY_ACTIVE_BRANCH
        else:
            branch = None

        logger.debug(f"Cloning {branch=}")

        if self.SOURCE_REPOSITORY_TYPE == "local":
            with porcelain.open_repo_closing(
                path_or_repo=self.SOURCE_REPOSITORY_PATH_OR_URL
            ) as repo_obj:
                repo_obj.clone(
                    target_path=f"{local_path.resolve()}",
                    branch=branch,
                    mkdir=False,
                    checkout=True,
                    progress=None,
                )
        elif self.SOURCE_REPOSITORY_TYPE == "remote":
            repo_obj = porcelain.clone(
                source=self.SOURCE_REPOSITORY_PATH_OR_URL,
                target=f"{local_path.resolve()}",
                branch=branch,
            )
        else:
            raise NotImplementedError(f"{self.SOURCE_REPOSITORY_TYPE} is not supported")

        gobj = repo_obj.get_object(repo_obj.head())
        logger.debug(
            f"Active branch: {porcelain.active_branch(repo_obj)}. "
            f"Latest commit cloned: {gobj.sha().hexdigest()} by {gobj.author}"
            f" at {gobj.commit_time}."
        )
        return repo_obj

    def _fetch(self, local_path: Path) -> Repo:
        """Fetch the remote repository from the existing local repository.

        Args:
            local_path (Path): path to the folder where to fetch

        Returns:
            Repo: the local repository object
        """
        # with porcelain.open_repo_closing(str(local_path.resolve())) as local_repo:
        logger.info(
            f"Fetching repository {self.SOURCE_REPOSITORY_PATH_OR_URL} to {local_path}",
        )
        local_repo = Repo(root=f"{local_path.resolve()}")
        porcelain.fetch(
            repo=f"{local_path.resolve()}",
            remote_location=self.SOURCE_REPOSITORY_PATH_OR_URL,
            force=True,
            prune=True,
            prune_tags=True,
            depth=0,
        )
        logger.debug(
            f"Repository {local_path.resolve()} has been fetched from "
            f"remote {self.SOURCE_REPOSITORY_PATH_OR_URL}. "
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
            f"Pulling repository {self.SOURCE_REPOSITORY_PATH_OR_URL} to {local_path}"
        )
        porcelain.pull(
            repo=local_path,
            remote_location=self.SOURCE_REPOSITORY_PATH_OR_URL,
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
