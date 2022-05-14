#! python3  # noqa: E265

"""
    Define toolbelt constant types and values.

    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from dataclasses import dataclass
from os.path import expandvars
from pathlib import Path
from typing import NamedTuple, Tuple

# #############################################################################
# ########## Classes ###############
# ##################################


@dataclass
class OSConfiguration:
    """Settings related to QGIS and depending on operating system"""

    profiles_path: Path
    shortcut_extension: str
    shortcut_forbidden_chars: Tuple[str] = None
    shortcut_icon_extensions: Tuple["str"] = ("ico",)


# #############################################################################
# ########## Classes ###############
# ##################################

OS_CONFIG: dict = {
    "darwin": OSConfiguration(
        profiles_path=Path(
            Path.home() / "Library/Application Support/QGIS/QGIS3/profiles/"
        ),
        shortcut_extension="app",
        shortcut_icon_extensions=("icns",),
    ),
    "linux": OSConfiguration(
        profiles_path=Path(Path.home() / ".local/share/QGIS/QGIS3/profiles/"),
        shortcut_extension=".desktop",
        shortcut_icon_extensions=("ico", "svg", "png"),
    ),
    "win32": OSConfiguration(
        profiles_path=Path(expandvars("%APPDATA%/Roaming/QGIS/QGIS3/profiles")),
        shortcut_extension=".lnk",
        shortcut_forbidden_chars=("<", ">", ":", '"', "/", "\\", "|", "?", "*"),
        shortcut_icon_extensions=("ico",),
    ),
}
