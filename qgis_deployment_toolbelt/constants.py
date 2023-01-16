#! python3  # noqa: E265

"""
    Define toolbelt constant types and values.

    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from dataclasses import dataclass
from functools import lru_cache
from os import PathLike, getenv
from os.path import expanduser, expandvars
from pathlib import Path
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

    profiles_path: Path = getenv("QGIS_CUSTOM_CONFIG_PATH")
    shortcut_extension: str = None
    shortcut_forbidden_chars: Tuple[str] = None
    shortcut_icon_extensions: Tuple[str] = None

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
        profiles_path=Path(
            getenv(
                "QGIS_CUSTOM_CONFIG_PATH",
                Path.home() / "Library/Application Support/QGIS/QGIS3/profiles/",
            )
        ),
        shortcut_extension="app",
        shortcut_icon_extensions=("icns",),
    ),
    "linux": OSConfiguration(
        profiles_path=Path(
            getenv(
                "QGIS_CUSTOM_CONFIG_PATH",
                Path.home() / ".local/share/QGIS/QGIS3/profiles/",
            )
        ),
        shortcut_extension=".desktop",
        shortcut_icon_extensions=("ico", "svg", "png"),
    ),
    "win32": OSConfiguration(
        profiles_path=Path(
            getenv(
                "QGIS_CUSTOM_CONFIG_PATH", expandvars("%APPDATA%/QGIS/QGIS3/profiles")
            )
        ),
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
