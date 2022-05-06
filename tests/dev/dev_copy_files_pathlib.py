#! python3  # noqa: E265
import shutil
from pathlib import Path
from shutil import copy, copy2, copyfile, copytree

t = Path("requirements.txt")
# move a file
# t.rename("tests/requirements.txt")

# move and override
# t.replace("tests/requirements.txt")

# copy using globbing
src = Path("tests")
dest = Path("/tmp/test/python-pathlib-copy")
dest.mkdir(parents=True, exist_ok=True)
for f in src.glob("**/*"):
    if f.is_dir():
        continue

    final_path = dest / f.relative_to(src)
    final_path.parent.mkdir(parents=True, exist_ok=True)
    # keeping file stats - needs a folderpath
    # copy2(f, final_path.parent)
    # as fast as possible but stats not guarantees - needs a filepath
    copyfile(f, final_path)

# using copytree
dest = Path("/tmp/test/python-shutil-copytree")
# keeping file stats
shutil.copytree(src, dest, copy_function=copy2)
# as fast as possible but stats not guarantees
shutil.copytree(src, dest, copy_function=copyfile)
