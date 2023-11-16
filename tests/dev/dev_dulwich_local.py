import logging
import tempfile
from pathlib import Path
from shutil import rmtree
from time import sleep

from dulwich import porcelain
from dulwich.repo import Repo

from qgis_deployment_toolbelt.profiles.local_git_handler import LocalGitHandler

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s||%(levelname)s||%(module)s||%(lineno)d||%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# source local repository
src_local_repo_path = Path("/home/jmo/Git/Geotribu/profils-qgis")

# -- WITH DULWICH --

dst_local_repo_path_dulwich = Path("tests/fixtures/tmp/dulwich-test-local/")
dst_local_repo_path_dulwich.mkdir(parents=True, exist_ok=True)

# src_repo = porcelain.open_repo(src_local_repo_path)

# # print(src_repo.get_description(), dir(src_repo))

# dst_repo_dulwich = src_repo.clone(
#     dst_local_repo_path_dulwich, mkdir=False, checkout=True, progress=None
# )
# gobj = dst_repo_dulwich.get_object(dst_repo_dulwich.head())
# print(
#     f"{dst_repo_dulwich}. Active branch: {str(porcelain.active_branch(dst_repo_dulwich))}. "
#     f"Latest commit cloned: {gobj.sha().hexdigest()} by {gobj.author}"
#     f" at {gobj.commit_time}."
# )
# src_repo.close()


# with porcelain.open_repo_closing(path_or_repo=src_local_repo_path) as repo_obj:
#     repo_obj.clone(
#         target_path=dst_local_repo_path_dulwich,
#         mkdir=False,
#         checkout=True,
#         progress=None,
#         branch=b"main",
#     )
# gobj = repo_obj.get_object(repo_obj.head())
# print(
#     f"{repo_obj}. Active branch: {str(porcelain.active_branch(repo_obj))}. "
#     f"Latest commit cloned: {gobj.sha().hexdigest()} by {gobj.author}"
#     f" at {gobj.commit_time}."
# )

# -- WITH QDT --

dst_local_repo_path_qdt = Path("tests/fixtures/tmp/dulwich-test-local-with-qdt/")

local_git_handler = LocalGitHandler(
    source_repository_path_or_uri=src_local_repo_path,
    branch_to_use="ddddd",
)
assert local_git_handler.SOURCE_REPOSITORY_PATH_OR_URL == src_local_repo_path
assert isinstance(
    local_git_handler.SOURCE_REPOSITORY_PATH_OR_URL, Path
), "source path or URL should be a Path"

assert local_git_handler.SOURCE_REPOSITORY_ACTIVE_BRANCH == "main"

target_repo = local_git_handler.download(destination_local_path=dst_local_repo_path_qdt)
assert isinstance(target_repo, Repo)

print("\n\nlet's try to fetch and pull")
target_repo2 = local_git_handler.download(
    destination_local_path=dst_local_repo_path_qdt
)

print("\n\nTRY in a temporary folder")
local_git_handler = LocalGitHandler(
    source_repository_path_or_uri=src_local_repo_path,
    branch_to_use="test/not-here",
)

with tempfile.TemporaryDirectory(
    prefix="QDT_test_local_git_",
    ignore_cleanup_errors=True,
    suffix="_specified_branch_existing",
) as tmpdirname:
    tempo_folder = Path(tmpdirname)
    print(tempo_folder.resolve(), tempo_folder.exists(), tempo_folder.is_dir())
    target_repo = local_git_handler.download(
        destination_local_path=tempo_folder.resolve()
    )
    print(target_repo)
    assert isinstance(target_repo, Repo)

# -- CLEAN UP --
print("\n3 seconds before cleaning up...")
sleep(3)
rmtree(dst_local_repo_path_dulwich, True)
rmtree(dst_local_repo_path_qdt, True)
