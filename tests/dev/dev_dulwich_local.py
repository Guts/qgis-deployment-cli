from pathlib import Path

from dulwich import porcelain

src_local_repo_path = Path("/home/jmo/Git/Geotribu/profils-qgis")
src_local_repo_path = Path("/home/jmo/Git/Geotribu/profils-qgis")

dst_local_repo_path = Path("/tmp/qdt-dev/dulwich-testdd/")
dst_local_repo_path.mkdir(parents=True, exist_ok=True)

src_repo = porcelain.open_repo(src_local_repo_path)

# print(src_repo.get_description(), dir(src_repo))

dst_repo = src_repo.clone(
    dst_local_repo_path, mkdir=False, checkout=True, progress=None
)
print(dst_repo)
