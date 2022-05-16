#! python3  # noqa: E265
from os.path import expandvars
from pathlib import Path

from pycrosskit.shortcuts import Shortcut

# Will Create shortcut
# * at Desktop if desktop is True
# * at Start Menu if start_menu is True

bin_path = Path(expandvars("%PROGRAMFILES%/QGIS-LTR/bin/qgis-ltr-bin.exe")).resolve()
print(bin_path, bin_path.exists())

Shortcut.delete(shortcut_name="QGIS Test script", desktop=True, start_menu=True)

Shortcut(
    shortcut_name="QGIS Test script",
    exec_path=str(
        Path(expandvars(r"%PROGRAMFILES%\QGIS-LTR\bin\qgis-ltr-bisn.exe")).resolve()
    ),
    description="QGIS raccourci créé par script",
    icon_path=str(Path(expandvars(r"%USERPROFILE%\OneDrive\Images\qgis_93837.ico"))),
    desktop=True,
    start_menu=True,
    work_dir=str(Path(expandvars(r"%PROGRAMFILES%\QGIS-LTR\bin")).resolve()),
)

# Will Delete shortcut
# * at Desktop if desktop is True
# * at Start Menu if start_menu is True
# Shortcut.delete(shortcut_name="My Spaghetti Shortcut", desktop=True, start_menu=True)
