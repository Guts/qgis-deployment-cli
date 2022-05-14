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
from pathlib import Path
from sys import platform as opersys
from typing import Tuple, Union

# Imports depending on operating system
if opersys == "win32":
    """windows"""
    import win32com.client
    from win32comext.shell import shell, shellcon
else:
    pass

from qgis_deployment_toolbelt.__about__ import __title__, __version__
from qgis_deployment_toolbelt.constants import OS_CONFIG

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
        exec_arguments: Tuple[str] = None,
        description: str = None,
        icon_path: Union[str, Path] = None,
        work_dir: Union[str, Path] = None,
    ):
        """Initialize a shortcut object.

        :param str name: name of the shortcut that will be created
        :param Union[str, Path] exec_path: path to the executable (which should exist)
        :param Tuple[str] exec_arguments: list of arguments and options to pass to the executable, defaults to None
        :param str description: shortcut description, defaults to None
        :param Union[str, Path] icon_path: path to icon .ico, defaults to None
        :param Union[str, Path] work_dir: current folder where to start the executable, defaults to None

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
            if any([i in name for i in self.os_config.shortcut_forbidden_chars]):
                raise ValueError(f"Shortcut name {name} contains invalid characters.")
            self.name = name
        else:
            raise TypeError(f"Shortcut name must be a string, not {type(name)}.")

        if isinstance(exec_path, (str, Path)):
            self.exec_path = Path(exec_path)
            if not self.exec_path.exists():
                logger.warning(f"Executable does not exist: {self.exec_path}")
        else:
            raise TypeError(
                f"exec_path must be a string or pathlib.Path, not {type(exec_path)}"
            )

        # optional
        if not description or isinstance(description, str):
            self.description = description
        else:
            raise TypeError(
                f"If defined, description must be a string, not {type(description)}"
            )

        if not exec_arguments or isinstance(exec_arguments, (tuple, list)):
            self.exec_arguments = " ".join(exec_arguments)
        else:
            raise TypeError(
                f"If defined, exec_arguments must be a tuple or list, not {type(exec_arguments)}"
            )
        if not icon_path or isinstance(icon_path, (str, Path)):
            self.icon_path = Path(icon_path)
            if not self.icon_path.exists():
                logger.warning(f"Icon does not exist: {self.exec_path}")
        else:
            raise TypeError(
                f"If defined, icon_path must be a string or pathlib.Path, not {type(icon_path)}"
            )
        if not work_dir or isinstance(work_dir, (str, Path)):
            self.work_dir = Path(work_dir)
            if not self.work_dir.exists():
                logger.warning(f"Work folder does not exist: {self.work_dir}")
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
            raise TypeError(f"desktop must be a boolean, not {type(desktop)}")
        if isinstance(start_menu, bool):
            self.start_menu = start_menu
        else:
            raise TypeError(f"start_menu must be a boolean, not {type(start_menu)}")

        if opersys == "win32":
            return self.win32_create()

    @staticmethod
    def delete(
        name: str, desktop: bool = False, start_menu: bool = False
    ) -> Tuple[str, str]:
        """Remove existing Shortcut from the system.

        :param str name: Name of shortcut
        :param bool desktop: Delete Shortcut on Desktop
        :param bool start_menu: Delete Shortcut on Start Menu

        :return: desktop and start menu path
        :return Tuple[str, str]: desktop_path, start menu path
        """
        if os.name == "nt":
            from pycrosskit.shortcut_platforms.windows import delete_shortcut
        else:
            from pycrosskit.shortcut_platforms.linux import delete_shortcut

        return delete_shortcut(name, desktop, start_menu)

    # -- PROPERTIES --------------------------------------------------------------
    @property
    def desktop_path(self) -> Path:
        """Return the user Desktop folder.

        :return Path: path to the Desktop folder
        """
        if opersys == "win32":
            return Path(shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0))

    @property
    def homedir_path(self) -> Path:
        """Return home directory.

        For Windows, note that we return CSIDL_PROFILE, not CSIDL_APPDATA,
        CSIDL_LOCAL_APPDATA or CSIDL_COMMON_APPDATA.

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

        For Windows, note that we return CSIDL_PROGRAMS not CSIDL_COMMON_PROGRAMS.

        :return Path: path to the Start Menu Programs folder
        """
        if opersys == "win32":
            return Path(shell.SHGetFolderPath(0, shellcon.CSIDL_PROGRAMS, None, 0))
        elif opersys == "linux":
            return self.homedir_path / ".local/share/applications"
        elif opersys == "darwin":
            return None
        else:
            logger.error(f"Unrecognized operating system: {opersys}.")
            return None

    # -- PRIVATE --------------------------------------------------------------
    def win32_create(self) -> Tuple[Union[Path, None], Union[Path, None]]:
        """Creates shortcut on Windows.

        :return: desktop and startmenu path
        :rtype: Tuple[Union[Path, None], Union[Path, None]]
        """
        # variable
        _WSHELL = win32com.client.Dispatch("Wscript.Shell")

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
            wscript.Description = self.description
            if self.icon_path is not None:
                wscript.IconLocation = str(self.icon_path.resolve())
            wscript.save()
        else:
            shortcut_start_menu_path = None

        return (shortcut_desktop_path, shortcut_start_menu_path)

    # def win32_delete_shortcut(
    #     name: str, startmenu: bool = False, desktop: bool = False
    # ) -> Tuple[str, str]:
    #     """Remove shortcut from the system.

    #     :param str name: Shortcut Object
    #     :param bool startmenu: True to create Start Menu Shortcut, defaults to False
    #     :param bool desktop: True to create Desktop Shortcut, defaults to False

    #     :return Tuple[str, str]: desktop_path, startmenu_path
    #     """
    #     user_folders = get_folders()
    #     desktop_path, startmenu_path = "", ""
    #     if startmenu:
    #         startmenu_path = str(Path(user_folders.startmenu) / (name + scut_ext))
    #         if os.path.exists(startmenu_path):
    #             os.chmod(startmenu_path, stat.S_IWRITE)
    #             os.remove(startmenu_path)
    #     if desktop:
    #         desktop_path = str(Path(user_folders.desktop) / (name + scut_ext))
    #         if os.path.exists(desktop_path):
    #             os.chmod(desktop_path, stat.S_IWRITE)
    #             os.remove(desktop_path)
    #     return desktop_path, startmenu_path