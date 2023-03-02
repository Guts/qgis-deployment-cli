#! python3  # noqa: E265

"""
    Cross-platform shortcuts manager. Derived from pycrosskit, by  Jiri Otoupal.
    See also: https://github.com/newville/pyshortcuts/
    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################
# standard
import logging
import os
import re
import stat
from pathlib import Path
from string import Template
from sys import platform as opersys
from typing import Iterable, Tuple, Union

# 3rd party

# Imports depending on operating system
if opersys == "win32":
    """windows"""
    import pythoncom
    import win32com.client
    from win32comext.shell import shell, shellcon
elif opersys == "linux":
    import distro
else:
    pass

from qgis_deployment_toolbelt.__about__ import __title__, __version__
from qgis_deployment_toolbelt.constants import OS_CONFIG
from qgis_deployment_toolbelt.utils.check_path import check_path
from qgis_deployment_toolbelt.utils.slugger import sluggy

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################


class ApplicationShortcut:
    def __init__(
        self,
        name: str,
        exec_path: Union[str, Path],
        exec_arguments: Iterable[str] = None,
        description: str = None,
        icon_path: Union[str, Path] = None,
        work_dir: Union[str, Path] = None,
    ):
        """Initialize a shortcut object.

        :param str name: name of the shortcut that will be created
        :param Union[str, Path] exec_path: path to the executable (which should exist)
        :param Iterable[str] exec_arguments: list of arguments and options to pass to the executable, defaults to None
        :param str description: shortcut description, defaults to None
        :param Union[str, Path] icon_path: path to icon file, defaults to None
        :param Union[str, Path] work_dir: current folder where to start the executable, defaults to None. In QDT, it's the profile folder.
        """
        # retrieve operating system specific configuration
        if opersys not in OS_CONFIG:
            raise OSError(
                f"Your operating system {opersys} is not supported. "
                f"Supported platforms: {','.join(OS_CONFIG.keys())}."
            )
        self.os_config = OS_CONFIG.get(opersys)

        # -- CHECK TYPE AND STORE ATTRIBUTES
        # mandatory
        if isinstance(name, str):
            if not self.os_config.valid_shortcut_name(name):
                raise ValueError(f"Shortcut name {name} contains invalid characters.")
            self.name = name
        else:
            raise TypeError(f"Shortcut name must be a string, not {type(name)}.")

        if isinstance(exec_path, (str, Path)):
            self.exec_path = Path(exec_path)
            if not self.exec_path.exists():
                # helper to handle common typo error on executable name on Windows
                if (
                    self.exec_path.name.endswith("qgis-bin.exe")
                    and self.exec_path.with_name("qgis-ltr-bin.exe").exists()
                ):
                    logger.warning(
                        f"Executable set does not exist: {self.exec_path} "
                        f"but {self.exec_path.with_name('qgis-ltr-bin.exe')} does, so "
                        "this one will be used instead. Check and fix your scenario."
                    )
                    self.exec_path = self.exec_path.with_name("qgis-ltr-bin.exe")
                elif (
                    self.exec_path.name.endswith("qgis-ltr-bin.exe")
                    and self.exec_path.with_name("qgis-bin.exe").exists()
                ):
                    logger.warning(
                        f"Executable set does not exist: {self.exec_path} "
                        f"but {self.exec_path.with_name('qgis-bin.exe')} does, so "
                        "this one will be used instead. Check and fix your scenario."
                    )
                    self.exec_path = self.exec_path.with_name("qgis-bin.exe")
                else:
                    logger.warning(
                        f"Executable does not exist: {self.exec_path}. "
                        "Shortcuts might not work. Check and fix your scenario."
                    )
        else:
            raise TypeError(
                f"exec_path must be a string or pathlib.Path, not {type(exec_path)}"
            )

        # optional
        if isinstance(exec_arguments, (tuple, list, type(None))):
            self.exec_arguments = self.check_exec_arguments(exec_arguments)
        else:
            raise TypeError(
                f"If defined, exec_arguments must be a tuple or list, not {type(exec_arguments)}"
            )
        if isinstance(description, (str, type(None))):
            self.description = description
        else:
            raise TypeError(
                f"If defined, description must be a string, not {type(description)}"
            )
        if isinstance(icon_path, (str, Path, type(None))):
            self.icon_path = self.check_icon_path(icon_path)
        else:
            raise TypeError(
                f"If defined, icon_path must be a string or pathlib.Path, not {type(icon_path)}"
            )
        if isinstance(work_dir, (str, Path, type(None))):
            self.work_dir = self.check_work_dir(work_dir)
        else:
            raise TypeError(
                f"If defined, work_dir must be a string or pathlib.Path, not {type(work_dir)}"
            )

    def create(
        self,
        desktop: bool = False,
        start_menu: bool = False,
    ) -> Tuple[str, str]:
        """Creates Shortcut

        :param bool desktop: True to generate a Desktop shortcut, defaults to False
        :param bool start_menu: True to generate a 'Start Menu' shortcut, defaults to False

        :return Tuple[str, str]: desktop and startmenu path
        """
        if isinstance(desktop, bool):
            self.desktop = desktop
        else:
            raise TypeError(f"'desktop' option must be a boolean, not {type(desktop)}")
        if isinstance(start_menu, bool):
            self.start_menu = start_menu
        else:
            raise TypeError(
                f"'start_menu' option must be a boolean, not {type(start_menu)}"
            )

        if not desktop and not start_menu:
            logger.debug(
                "Shortcut will not be created because both desktop and start "
                "menu options are False."
            )
            return (None, None)

        if opersys == "win32":
            return self.win32_create()
        elif opersys == "linux":
            return self.freedesktop_create()
        else:
            pass

    def check_exec_arguments(
        self, exec_arguments: Union[Iterable[str], None]
    ) -> Union[Tuple[str], None]:
        """Check if exec_arguments are valid.

        :param Union[Iterable[str], None] exec_arguments: input executable arguments to check

        :return Union[Tuple[str], None]: tuple of arguments
        """
        if not exec_arguments:
            return None
        # store as path
        return " ".join(exec_arguments)

    def check_icon_path(self, icon_path: Union[str, Path, None]) -> Union[Path, None]:
        """Check icon path and return full path if it exists.

        :param Union[str, Path] icon_path: input icon path to check

        :return Union[Path, None]: icon path as Path if str or Path, else None
        """
        if not icon_path:
            return None
        # store as path
        icon_path = Path(icon_path)
        # checks
        if check_path(
            input_path=icon_path,
            must_be_a_file=True,
            must_be_readable=True,
            must_exists=True,
            raise_error=False,
        ):
            return icon_path.resolve()
        else:

            logger.warning(f"Icon does not exist: {icon_path}")
            return None

    def check_work_dir(self, work_dir: Union[str, Path, None]) -> Union[Path, None]:
        """Check work dir and return full path if it exists.

        :param Union[str, Path] work_dir: input work dir to check

        :return Union[Path, None]: work dir as Path if str or Path, else None
        """
        if not work_dir:
            return None
        # store as path
        work_dir = Path(work_dir)
        # checks
        if work_dir.is_dir():
            return work_dir.resolve()
        else:
            logger.warning(f"Work folder does not exist: {work_dir}")
            return None

    # -- PROPERTIES --------------------------------------------------------------
    @property
    def desktop_path(self) -> Path:
        """Return the user Desktop folder.

        Partly inspired from https://stackoverflow.com/a/13742626/2556577.

        Returns:
            Path: path to the current user Desktop folder.
        """
        default_value = Path(Path.home(), "Desktop")

        if opersys == "win32":
            return Path(shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0))
        elif opersys in ("darwin", "linux"):
            # have a look to XDG configuration file with user folders
            config_xdg_user_dirs = Path(self.homedir_path, ".config", "user-dirs.dirs")
            is_config_file_usable = check_path(
                input_path=config_xdg_user_dirs,
                must_be_a_file=True,
                must_be_readable=True,
                must_exists=True,
                raise_error=False,
            )
            if is_config_file_usable:
                with config_xdg_user_dirs.open("r") as bf_config:
                    data = bf_config.read()

                desktop_paths = re.findall('XDG_DESKTOP_DIR="([^"]*)', data)
                if len(desktop_paths):
                    return Path(
                        re.sub(r"\$HOME", os.path.expanduser("~"), desktop_paths[0])
                    )

            return default_value
        else:

            logger.warning(
                f"Unrecognized operating system ({opersys}) so path to the "
                f"user desktop is using a fallback value: {default_value}"
            )
            return default_value

    @property
    def homedir_path(self) -> Path:
        """Return home directory.

        For Windows, note that we return `CSIDL_PROFILE`, not `CSIDL_APPDATA`,
        `CSIDL_LOCAL_APPDATA` or `CSIDL_COMMON_APPDATA`.
        See: https://www.nirsoft.net/articles/find_special_folder_location.html
        TODO: evaluate use of platformdirs

        :return Path: path to the user home
        """
        if opersys == "win32":
            return Path(shell.SHGetFolderPath(0, shellcon.CSIDL_PROFILE, 0, 0))
        elif opersys == "linux":
            home = None
            try:
                home = Path.home()
            except RuntimeError as err:
                logger.debug("Home directory can’t be resolved with pathlib: %s", err)
            # try another way
            if home is None:
                home = os.path.expanduser("~")
            if home is None:
                home = os.path.normpath(os.environ.get("HOME", os.path.abspath(".")))
            return Path(home)
        elif opersys == "darwin":
            return Path(os.path.expanduser("~"))
        else:
            logger.error(f"Unrecognized operating system: {opersys}.")
            return None

    @property
    def startmenu_path(self) -> Path:
        """Return user Start Menu Programs folder.

        For Windows, note that we return `CSIDL_PROGRAMS` not `CSIDL_COMMON_PROGRAMS`.

        :return Path: path to the Start Menu Programs folder
        """
        if opersys == "win32":
            return Path(shell.SHGetFolderPath(0, shellcon.CSIDL_PROGRAMS, None, 0))
        elif opersys == "linux":
            return self.homedir_path / ".local/share/applications"
        elif opersys == "darwin":
            return self.homedir_path / ".local/share/applications"
        else:
            logger.error(f"Unrecognized operating system: {opersys}.")
            return None

    # -- PRIVATE --------------------------------------------------------------
    def freedesktop_create(self) -> Tuple[Union[Path, None], Union[Path, None]]:
        """Creates shortcut on distributions using FreeDesktop.

        :return: desktop and startmenu path
        :rtype: Tuple[Union[Path, None], Union[Path, None]]
        """
        # prepare shortcut
        template_shortcut = Path(__file__).parent / "shortcut_freedesktop.template"
        check_path(
            input_path=template_shortcut,
            must_be_a_file=True,
            must_be_readable=True,
            must_exists=True,
        )

        # load template
        with template_shortcut.open("r", encoding="UTF-8") as bf_tpl:
            tpl = Template(bf_tpl.read())

        # handle case where work dir is not defined
        if isinstance(self.work_dir, Path):
            profile_name = self.work_dir.name
        else:
            profile_name = "default"

        # subsitute with values
        shortcut_text = tpl.safe_substitute(
            {
                "description": self.description,
                "exec": f"{self.exec_path} {self.exec_arguments}",
                "icon_path": self.icon_path,
                "profile_folder": str(self.work_dir),
                "profile_name": profile_name,
                "shortcut_name": self.name,
            }
        )

        # desktop shortcut
        if self.desktop:

            self.desktop_path.mkdir(parents=True, exist_ok=True)

            # create shortcut
            shortcut_desktop_path = Path(
                self.desktop_path,
                f"qdt.{sluggy(profile_name, '.')}.qgis.desktop",
            )
            shortcut_desktop_path.write_text(shortcut_text, encoding="UTF-8")
            shortcut_desktop_path.chmod(
                shortcut_desktop_path.stat().st_mode
                | (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH),
                follow_symlinks=True,
            )
        else:
            shortcut_desktop_path = None

        # create required shortcut
        if self.start_menu:
            self.startmenu_path.mkdir(parents=True, exist_ok=True)
            # create shortcut
            shortcut_start_menu_path = Path(
                self.startmenu_path,
                f"qdt.{sluggy(profile_name, '.')}.qgis.desktop",
            )
            shortcut_start_menu_path.write_text(shortcut_text, encoding="UTF-8")
            shortcut_start_menu_path.chmod(
                shortcut_start_menu_path.stat().st_mode
                | (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH),
                follow_symlinks=True,
            )
        else:
            shortcut_start_menu_path = None

        return (shortcut_desktop_path, shortcut_start_menu_path)

    def win32_create(self) -> Tuple[Union[Path, None], Union[Path, None]]:
        """Creates shortcut on Windows.

        :return: desktop and startmenu path
        :rtype: Tuple[Union[Path, None], Union[Path, None]]
        """
        # variable
        _WSHELL = win32com.client.Dispatch("Wscript.Shell", pythoncom.CoInitialize())

        # desktop shortcut
        if self.desktop:
            shortcut_desktop_path = (
                self.desktop_path / f"{self.name}{self.os_config.shortcut_extension}"
            )

            wscript = _WSHELL.CreateShortCut(str(shortcut_desktop_path.resolve()))
            if self.exec_arguments:
                wscript.Arguments = self.exec_arguments
            wscript.Targetpath = str(self.exec_path.resolve())
            if self.work_dir:
                wscript.WorkingDirectory = str(self.work_dir.resolve())
            wscript.WindowStyle = 0
            if self.description:
                wscript.Description = self.description
            else:
                wscript.Description = f"Created by {__title__} {__version__}"
            if self.icon_path:
                wscript.IconLocation = str(self.icon_path.resolve())
            wscript.save()
        else:
            shortcut_desktop_path = None

        # start menu shortcut
        if self.start_menu:
            shortcut_start_menu_path = (
                self.startmenu_path / f"{self.name}{self.os_config.shortcut_extension}"
            )

            wscript = _WSHELL.CreateShortCut(str(shortcut_start_menu_path.resolve()))
            if self.exec_arguments:
                wscript.Arguments = self.exec_arguments
            wscript.Targetpath = str(self.exec_path.resolve())
            if self.work_dir is not None:
                wscript.WorkingDirectory = str(self.work_dir.resolve())
            wscript.WindowStyle = 0
            if self.description:
                wscript.Description = self.description
            else:
                wscript.Description = f"Created by {__title__} {__version__}"
            if self.icon_path is not None:
                wscript.IconLocation = str(self.icon_path.resolve())
            wscript.save()
        else:
            shortcut_start_menu_path = None

        return (shortcut_desktop_path, shortcut_start_menu_path)


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    if opersys == "linux" and distro.name() in ("Ubuntu", "Kubuntu"):
        qgis_shortcut = ApplicationShortcut(
            "QDT",
            exec_path="/home/jmo/.local/bin/qdeploy-toolbelt",
            exec_arguments=[
                "-v",
            ],
            description="Launch QGIS Deployment Toolbelt with the scenario located "
            "into the local repository.",
            work_dir=Path(__file__).parent.parent,
        )

        print(
            type(qgis_shortcut.homedir_path),
            qgis_shortcut.homedir_path,
        )
        print(type(qgis_shortcut.desktop_path), qgis_shortcut.desktop_path)
        print(type(qgis_shortcut.startmenu_path), qgis_shortcut.startmenu_path)

        qgis_shortcut.create()
