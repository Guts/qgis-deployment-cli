#! python3  # noqa: E265

"""
    Define toolbelt constant types and values.

    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from os.path import expandvars
from pathlib import Path
from typing import NamedTuple

# #############################################################################
# ########## Classes ###############
# ##################################


class OSConfiguration(NamedTuple):
    """Settings related to QGIS and depending on operating system"""

    profiles_path: Path


# #############################################################################
# ########## Classes ###############
# ##################################

OS_CONFIG: dict = {
    "darwin": OSConfiguration(
        profiles_path=Path("~/Library/Application Support/QGIS/QGIS3/profiles/")
    ),
    "linux": OSConfiguration(profiles_path=Path("~/.local/share/QGIS/QGIS3/profiles/")),
    "windows": OSConfiguration(
        profiles_path=Path(expandvars("%APPDATA%/Roaming/QGIS/QGIS3/profiles"))
    ),
}
