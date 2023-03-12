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
from os import PathLike, getenv
from os.path import expanduser, expandvars
from pathlib import Path
from shutil import which

# package
from qgis_deployment_toolbelt.utils.check_path import check_path

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)

# #############################################################################
# ########## Functions #############
# ##################################


def get_qdt_working_directory(
    specific_value: PathLike = None, identifier: str = "default"
) -> Path:
    """Get QDT working directory.

    Args:
        specific_value (PathLike, optional): a specific path to use. If set it's \
            expanded and returned. Defaults to None.
        identifier (str, optional): used to make the folder unique. If not set, \
            'default' (sure, not so unique...) is used. Defaults to "default".

    Returns:
        Path: path to the QDT working directory
    """
    if specific_value:
        return Path(expandvars(expanduser(specific_value)))
    elif getenv("QDT_LOCAL_WORK_DIR"):
        return Path(expandvars(expanduser(getenv("QDT_LOCAL_WORK_DIR"))))
    else:
        return Path(
            expandvars(
                expanduser(
                    getenv(
                        "QDT_LOCAL_WORK_DIR",
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
    qgis_bin_exe_path: Path = None
    shortcut_extension: str = None
    shortcut_forbidden_chars: tuple[str] = None
    shortcut_icon_extensions: tuple[str] = None

    @property
    def get_qgis_bin_path(self) -> Path:
        """Returns the QGIS path determined from QDT_QGIS_EXE_PATH environment variable,
        or result of which command or fallback to default value passed to the object.

        Returns:
            Path: path to the QGIS bin/exe
        """
        if envvar := getenv("QDT_QGIS_EXE_PATH"):
            if envvar.startswith("{") and envvar.endswith("}"):
                try:
                    qdt_qgis_exe_path = ast.literal_eval(envvar)
                    if isinstance(qdt_qgis_exe_path, dict):
                        logger.debug(
                            f"'QDT_QGIS_EXE_PATH' is a valid dictionary: {envvar}"
                        )
                        for k, v in qdt_qgis_exe_path.items():
                            if k in self.names_alter + [self.name_python]:
                                logger.debug(
                                    f"QGIS path found in 'QDT_QGIS_EXE_PATH' dictionary: {v}"
                                )
                                return Path(expandvars(expanduser(v)))
                except Exception as err:
                    logger.error(
                        f"Failed to interpret 'QDT_QGIS_EXE_PATH' value: {envvar}."
                        f"Trace: {err}"
                    )
            elif check_path(
                input_path=envvar,
                must_exists=False,
                must_be_readable=False,
                raise_error=False,
            ):
                logger.debug(
                    f"'QDT_QGIS_EXE_PATH' is a simple string and a valid path: {envvar}"
                )
                return Path(expandvars(expanduser(envvar)))

            # fallback
            logger.warning(
                f"Unrecognised value format for 'QDT_QGIS_EXE_PATH': {envvar}. "
                "Fallback to default path: "
                f"{Path(expandvars(expanduser(self.qgis_bin_exe_path)))}"
            )
            return Path(expandvars(expanduser(self.qgis_bin_exe_path)))
        elif which_qgis_path := which("qgis"):
            logger.debug(f"QGIS path found using which: {which_qgis_path}")
            return Path(which_qgis_path)
        else:
            logger.debug(
                f"QGIS path not found, using default value: {self.qgis_bin_exe_path}"
            )
            return Path(expandvars(expanduser(self.qgis_bin_exe_path)))

    def valid_shortcut_name(self, shortcut_name: str) -> bool:
        """Check if a given string is a valid shortcut name for the current operating
        system.

        Args:
            shortcut_name (str): given shortcut name to check

        Returns:
            bool: True if the givn string can be used as shortcut name
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
        qgis_bin_exe_path=Path("/usr/bin/qgis"),
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
        qgis_bin_exe_path=Path("/usr/bin/qgis"),
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
        qgis_bin_exe_path=Path(
            expandvars(expanduser("%PROGRAMFILES%/QGIS 3.28.4/bin/qgis-ltr-bin.exe"))
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
