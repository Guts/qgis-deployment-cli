#! python3  # noqa: E265

"""
    QDT QGIS Profile object and related sugar.

    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# standard
import json
import logging
from pathlib import Path
from sys import platform as opersys
from sys import version_info

# Imports depending on Python version
if version_info[1] < 11:
    from typing_extensions import Self
else:
    from typing import Self

# Package
from qgis_deployment_toolbelt.constants import OS_CONFIG

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################
class QdtProfile:
    """Object definition for QGIS Profile handled by QDT."""

    ATTR_MAP = {
        "qgis_minimum_version": "qgisMinimumVersion",
        "qgis_maximum_version": "qgisMaximumVersion",
    }

    def __init__(
        self,
        alias: str = None,
        author: str = None,
        description: str = None,
        email: str = None,
        folder: Path = None,
        icon: str = None,
        json_ref_path: Path = None,
        loaded_from_json: bool = False,
        name: str = None,
        plugins: list = None,
        qgis_maximum_version: str = None,
        qgis_minimum_version: str = None,
        splash: str = None,
        version: str = None,
        **kwargs,
    ):
        """Initialize a QDT Profile object.

        :param str name: name of the shortcut that will be created
        :param str author: profile author name
        """
        # retrieve operating system specific configuration
        if opersys not in OS_CONFIG:
            raise OSError(
                f"Your operating system {opersys} is not supported. "
                f"Supported platforms: {','.join(OS_CONFIG.keys())}."
            )
        self.os_config = OS_CONFIG.get(opersys)

        # default values for the object attributes/properties
        self._alias = None
        self._author = None
        self._description = None
        self._email = None
        self._folder = None
        self._icon = None
        self._json_ref_path = None
        self._name = None
        self._splash = None
        self._plugins = None
        self._qgis_maximum_version = None
        self._qgis_minimum_version = None
        self._version = None

        # if values have been passed, so use them as objects attributes.
        # attributes are prefixed by an underscore '_'
        if alias:
            self._alias = alias
        if author:
            self._author = author
        if description:
            self._description = description
        if email:
            self._email = email
        if folder:
            self._folder = folder
        if icon:
            self._icon = icon
        if json_ref_path:
            self._json_ref_path = json_ref_path
        if name:
            self._name = name
        if plugins:
            self._plugins = plugins
        if qgis_maximum_version:
            self._qgis_maximum_version = qgis_maximum_version
        if qgis_minimum_version:
            self._qgis_minimum_version = qgis_minimum_version
        if splash:
            self._splash = splash
        if version:
            self._version = version

    @classmethod
    def from_json(cls, profile_json_path: Path) -> Self:
        """Load profile from a profile.json file.

        :param Path profile_json_path: path to the profile json file
        :return Self: QdtProfile

        :example:

            .. code-block:: python

                QdtProfile = QdtProfile.from_json(
                        Path(src_profile / "profile.json")
                    )
                print(profile._splash.resolve)

        """
        with profile_json_path.open(mode="r", encoding="utf8") as in_profile_json:
            profile_data = json.load(in_profile_json)

        for k, v in cls.ATTR_MAP.items():
            profile_data[k] = profile_data.pop(v, None)

        return cls(
            json_ref_path=profile_json_path, loaded_from_json=True, **profile_data
        )

    @property
    def alias(self) -> str:
        """Returns the alias for the QGIS profile.

        :return str: profile alias
        """
        return self._alias

    @property
    def folder(self) -> Path:
        """Returns the path to the folder where the profile is stored.

        :return str: profile folder path
        """
        if self._folder:
            return self._folder.parent.resolve()
        else:
            return self._folder

    @property
    def icon_path(self) -> Path:
        """Returns the path to the profile icon path.

        :return str: profile icon path
        """
        if self._folder and self._icon:
            return self._folder.joinpath(self._icon)

        return self.icon_path.resolve()

    @property
    def json_ref_path(self) -> Path:
        """Returns the path to the corresponding JSON path.

        :return str: profile json_ref_path path
        """
        return self._json_ref_path.resolve()

    @property
    def name(self) -> Path:
        """Returns the path to the name where the profile is stored.

        :return str: profile name path
        """
        return self._name

    @property
    def splash(self) -> str:
        """Returns the profile version as string.

        :return str: profile version.
        """
        return self._splash

    @property
    def version(self) -> str:
        """Returns the profile version as string.

        :return str: profile version.
        """
        return self._version
