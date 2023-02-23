#! python3  # noqa: E265

"""
    Define toolbelt constant types and values.

    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import ast
import logging
from dataclasses import dataclass
from functools import lru_cache
from os import PathLike, getenv
from os.path import expanduser, expandvars
from pathlib import Path
from shutil import which
from typing import Tuple

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)

# #############################################################################
# ########## Functions #############
# ##################################


@lru_cache(maxsize=128)
def get_qdt_working_directory(
    specific_value: PathLike = None, identifier: str = "default"
) -> Path:
    """Get QDT working directory.

    Args:
        specific_value (PathLike, optional): a specific path to use. If set it's \
            expanded and returned. Defaults to None.
        identifier (str, optional): used to make the folder unique. If not set, \
            'default' (sure, not so unique...) is used. Defaults to None.

    Returns:
        Path: path to the QDT working directory
    """
    if specific_value:
        return Path(expandvars(expanduser(specific_value)))
    elif getenv("QDT_PROFILES_PATH"):
        return Path(expandvars(expanduser(getenv("QDT_PROFILES_PATH"))))
    else:
        return Path(
            expandvars(
                expanduser(
                    getenv(
                        "LOCAL_QDT_WORKDIR",
                        f"~/.cache/qgis-deployment-toolbelt/{identifier}",
                    ),
                )
            )
        )


# #############################################################################
# ########## Classes ###############
# ##################################


@dataclass
class OSConfiguration:
    """Settings related to QGIS and depending on operating system"""

    name_python: str
    names_alter: list = None
    profiles_path: Path = getenv("QGIS_CUSTOM_CONFIG_PATH")
    qgis_bin_exe_path: str = None
    shortcut_extension: str = None
    shortcut_forbidden_chars: Tuple[str] = None
    shortcut_icon_extensions: Tuple[str] = None

    @property
    def get_qgis_bin_path(self) -> Path:
        """Returns the QGIS path determined from QDT_QGIS_EXE_PATH environment variable,
        or result of which command or fallback to default value passed to the object.

        Returns:
            Path: path to the QGIS bin/exe
        """
        if getenv("QDT_QGIS_EXE_PATH"):
            qdt_qgis_exe_path = ast.literal_eval(getenv("QDT_QGIS_EXE_PATH"))
            if isinstance(qdt_qgis_exe_path, str):
                return Path(expandvars(expanduser(getenv("QDT_QGIS_EXE_PATH"))))
            elif isinstance(qdt_qgis_exe_path, dict):
                for k, v in qdt_qgis_exe_path.items():
                    if k in self.names_alter + [self.name_python]:
                        return Path(expandvars(expanduser(v)))
            else:
                return qdt_qgis_exe_path
        elif which("qgis"):
            return Path(which("qgis"))
        else:
            return Path(expandvars(expanduser(self.qgis_bin_exe_path)))

    def valid_shortcut_name(self, shortcut_name: str) -> bool:
        """Check if a shortcut name is valid.

        :param str shortcut_name: _description_
        :return bool: _description_
        """
        if self.shortcut_forbidden_chars is None:
            return True
        for char in self.shortcut_forbidden_chars:
            if char in shortcut_name:
                logger.error(
                    f"Shortcut name '{shortcut_name}' contains forbidden char '{char}'"
                )
                return False
        return True


# #############################################################################
# ########## Main ##################
# ##################################

OS_CONFIG: dict = {
    "darwin": OSConfiguration(
        name_python="darwin",
        names_alter=["apple", "mac", "macos"],
        profiles_path=Path(
            getenv(
                "QGIS_CUSTOM_CONFIG_PATH",
                Path.home() / "Library/Application Support/QGIS/QGIS3/profiles/",
            )
        ),
        qgis_bin_exe_path="/usr/bin/qgis",
        shortcut_extension="app",
        shortcut_icon_extensions=("icns",),
    ),
    "linux": OSConfiguration(
        name_python="linux",
        names_alter=["kubuntu", "ubuntu"],
        profiles_path=Path(
            getenv(
                "QGIS_CUSTOM_CONFIG_PATH",
                Path.home() / ".local/share/QGIS/QGIS3/profiles/",
            )
        ),
        qgis_bin_exe_path="/usr/bin/qgis",
        shortcut_extension=".desktop",
        shortcut_icon_extensions=("ico", "svg", "png"),
    ),
    "win32": OSConfiguration(
        name_python="win32",
        names_alter=["win", "windows"],
        profiles_path=Path(
            getenv(
                "QGIS_CUSTOM_CONFIG_PATH", expandvars("%APPDATA%/QGIS/QGIS3/profiles")
            )
        ),
        qgis_bin_exe_path="%PROGRAMFILES%/QGIS/3_22/bin/qgis-ltr-bin.exe",
        shortcut_extension=".lnk",
        shortcut_forbidden_chars=("<", ">", ":", '"', "/", "\\", "|", "?", "*"),
        shortcut_icon_extensions=("ico",),
    ),
}

# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
