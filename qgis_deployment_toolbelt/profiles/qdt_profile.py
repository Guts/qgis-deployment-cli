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

# 3rd party
from packaging.version import InvalidVersion, Version

# Package
from qgis_deployment_toolbelt.constants import OS_CONFIG
from qgis_deployment_toolbelt.plugins.plugin import QgisPlugin
from qgis_deployment_toolbelt.utils.check_path import check_path

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

    # optional mapping on attributes names.
    # {attribute_name_in_output_object: attribute_name_from_input_file}  # noqa: E800
    ATTR_MAP = {
        "qgis_maximum_version": "qgisMaximumVersion",
        "qgis_minimum_version": "qgisMinimumVersion",
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

        # default values for immutable attributes
        self.loaded_from_json = loaded_from_json

        # default values for attributes/properties that can be get/set
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
    def from_json(cls, profile_json_path: Path, profile_folder: Path = None) -> Self:
        """Load profile from a profile.json file.

        :param Path profile_json_path: path to the profile json file
        :param Path profile_folder: path to the profile folder, defaults to None

        :return Self: QdtProfile object with attributes filled from JSON.

        :example:

            .. code-block:: python

                QdtProfile = QdtProfile.from_json(
                        Path(src_profile / "profile.json")
                    )
                print(profile.splash.resolve())

        """
        # checks
        check_path(
            input_path=profile_json_path,
            must_be_a_file=True,
            must_exists=True,
            must_be_readable=True,
        )
        if profile_folder:
            check_path(
                input_path=profile_folder,
                must_be_a_folder=True,
                must_exists=True,
                must_be_readable=True,
            )

        # load JSON
        with profile_json_path.open(mode="r", encoding="utf8") as in_profile_json:
            profile_data = json.load(in_profile_json)

        # map attributes names
        for k, v in cls.ATTR_MAP.items():
            profile_data[k] = profile_data.pop(v, None)

        # return new instance with loaded object
        return cls(
            folder=profile_folder,
            json_ref_path=profile_json_path,
            loaded_from_json=True,
            **profile_data,
        )

    @property
    def alias(self) -> str:
        """Returns the profile's alias.

        :return str: profile alias
        """
        return self._alias

    @property
    def folder(self) -> Path:
        """Returns the path to the folder where the profile is stored.

        :return Path: profile folder path
        """
        if isinstance(self._folder, Path):
            return self._folder.resolve()
        else:
            return self._folder

    @property
    def is_loaded_from_json(self) -> bool:
        """Tells if the profile has been loaded from a JSON file.

        :return bool: True if the profile has been loaded from a JSON file
        """
        return self.loaded_from_json

    @property
    def icon(self) -> str:
        """Returns the icon as specified into the original profile.json.

        :return str: profile icon value
        """
        if self._icon:
            return self._icon

    @property
    def icon_path(self) -> Path:
        """Returns the path to the profile's icon into the profile folder.

        :return Path: profile icon path
        """
        if self._folder and self._icon:
            return self._folder.joinpath(self._icon)

    @property
    def json_ref_path(self) -> Path:
        """Returns the path to the corresponding JSON path.

        :return Path: profile json_ref_path path
        """
        return self._json_ref_path.resolve()

    @property
    def name(self) -> str:
        """Returns the profile's name. If not set, the folder name is used.

        Returns:
            str: profile's name
        """
        if self._name:
            return self._name
        elif self._folder:
            return self._folder
        else:
            return None

    @property
    def path_in_qgis(self) -> Path:
        """Returns the path to the folder where the profile is stored in QGIS 3
            (= installed).

        Returns:
            Path: path to the installed (i.e. in QGIS) profile folder
        """
        return self.os_config.profiles_path / self.name

    @property
    def plugins(self) -> list[QgisPlugin]:
        """Returns the plugins associated with the profile.

        Returns:
            List[QgisPlugin]: list of plugins
        """
        if self._plugins:
            return [QgisPlugin.from_dict(p) for p in self._plugins]
        else:
            return []

    @property
    def splash(self) -> str | Path:
        """Returns the profile splash image as path if can be resolved or as string.

        Returns:
            Union[str, Path]: path to the profile splash image
        """
        if (
            self._splash
            and isinstance(self.folder, Path)
            and self.folder.joinpath(self._splash).is_file()
        ):
            return self.folder.joinpath(self._splash)
        else:
            return self._splash

    @property
    def version(self) -> str:
        """Returns the profile version as string.

        Returns:
            str: version
        """
        return self._version

    def is_older_than(self, version_to_compare: str | Self) -> bool:
        """Determine if the actual object version is older than the given version to
            compare.

        Args:
            version_to_compare (Union[str, Self]): given version to compare with object
            version

        Returns:
            bool: True if the given version is newer (more recent)
        """
        if not any([self.version, version_to_compare]):
            logger.error("Object version is not set, so the comparizon is impossible.")
            return None

        # if a profile is given
        if isinstance(version_to_compare, QdtProfile):
            # take the opportunity to check the name is the same
            if not self.name == version_to_compare.name:
                logger.warning(
                    "Be careful, the profile to compare seems to be different: "
                    f"{self.name} != {version_to_compare.name}"
                )
            # store the version string
            version_to_compare = version_to_compare.version

        # load object version as packaging.Version object
        try:
            profile_version = Version(self.version)
        except InvalidVersion as err:
            logger.error(
                f"Profile {self.name} uses an incompatible versioning scheme: {self.version}."
                "It's not Semver (even prefixed by 'v'), nor Calver or any of "
                "supported specification. See https://peps.python.org/pep-0440/. "
                f"Trace: {err}"
            )
            return None

        # load version to compare as packaging.Version object
        try:
            version_to_compare = Version(version_to_compare)
        except InvalidVersion as err:
            logger.error(
                f"Version to compare uses an incompatible versioning scheme: {self.version}."
                "It's not Semver (even prefixed by 'v'), nor Calver or any of "
                "supported specification. See https://peps.python.org/pep-0440/. "
                f"Trace: {err}"
            )
            return None

        logger.debug(f"Comparing versions: {profile_version} and {version_to_compare}")

        return profile_version < version_to_compare


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    profile_good_sample = Path("tests/fixtures/profiles/good_profile_complete.json")
    assert profile_good_sample.is_file() is True

    qdt_profile = QdtProfile.from_json(
        profile_json_path=profile_good_sample, profile_folder=profile_good_sample.parent
    )
    assert isinstance(qdt_profile, QdtProfile)
    assert isinstance(qdt_profile.plugins, list)
