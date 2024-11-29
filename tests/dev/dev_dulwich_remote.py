import logging
import tempfile
from pathlib import Path

from dulwich import porcelain
from dulwich.repo import Repo

from qgis_deployment_toolbelt.profiles.remote_git_handler import RemoteGitHandler

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s||%(levelname)s||%(module)s||%(lineno)d||%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


git_repository_remote_url = (
    "https://github.com/qgis-deployment/qgis-deployment-toolbelt-cli.git"
)
git_repository_local = Path(__file__).parent.parent.joinpath(
    "fixtures/tmp/dev_repository/"
)
# git_repository_local.mkdir(parents=True, exist_ok=True)

# # -- WITH DULWICH --
# print("\n\n-- WORKING WITH DULWICH --")
# git_repository_local_dulwich = git_repository_local.joinpath("dulwich")
# if (
#     git_repository_local_dulwich.is_dir()
#     and git_repository_local_dulwich.joinpath(".git").is_dir()
# ):
#     print(
#         f"{git_repository_local_dulwich.resolve()} is a git local project ---> let's FETCH then PULL"
#     )
#     dul_local_repo = Repo(root=f"{git_repository_local_dulwich.resolve()}")
#     porcelain.fetch(
#         repo=dul_local_repo,
#         remote_location=git_repository_remote_url,
#         force=True,
#         prune=True,
#     )

#     porcelain.pull(
#         repo=dul_local_repo,
#         remote_location=git_repository_remote_url,
#         force=True,
#         fast_forward=True,
#     )
# else:
#     git_repository_local_dulwich.mkdir(parents=True, exist_ok=True)
#     print(
#         f"{git_repository_local_dulwich.resolve()} is not a git local project ---> let's CLONE"
#     )
#     dul_local_repo = porcelain.clone(
#         source=git_repository_remote_url,
#         target=f"{git_repository_local_dulwich.resolve()}",
#     )

# # get local active branch
# active_branch = porcelain.active_branch(repo=dul_local_repo)
# print(f"\nLocal active branch {active_branch.decode()}")

# dul_local_repo.close()
# # assert dul_repo == dul_local_repo

# -- WITH QDT --
print("\n\n-- WORKING WITH QDT --")
git_repository_local_dulwich = git_repository_local.joinpath("with_qdt")
remote_git_handler = RemoteGitHandler(source_repository_url=git_repository_remote_url)
assert remote_git_handler.SOURCE_REPOSITORY_PATH_OR_URL == git_repository_remote_url
assert isinstance(remote_git_handler.SOURCE_REPOSITORY_PATH_OR_URL, str)

remote_git_handler.download(destination_local_path=git_repository_local_dulwich)

# good_git_url = "https://gitlab.com/Oslandia/qgis/profils_qgis_fr.git"
# remote_git_handler = RemoteGitHandler(source_repository_url=good_git_url)

# with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdirname:
#     local_dest = Path(tmpdirname) / "test_git_clone"
#     # clone
#     remote_git_handler.download(destination_local_path=local_dest)

#     # check pull is working
#     remote_git_handler.clone_or_pull(to_local_destination_path=local_dest)
