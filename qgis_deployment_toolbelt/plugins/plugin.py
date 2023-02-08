#! python3  # noqa: E265

"""
    Plugin object model.

    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################


# Standard library
import configparser
import logging
import zipfile
from dataclasses import dataclass, fields
from enum import Enum
from pathlib import Path
from sys import version_info
from typing import Union
from urllib.parse import quote, urlsplit, urlunsplit

# 3rd party
from packaging.version import InvalidVersion, Version

# package
from qgis_deployment_toolbelt.utils.check_path import check_path
from qgis_deployment_toolbelt.utils.slugger import sluggy

# Imports depending on Python version
if version_info[1] < 11:
    from typing_extensions import Self
else:
    from typing import Self

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)

# #############################################################################
# ########## Classes ###############
# ##################################


class QgisPluginLocation(Enum):
    local = 1
    remote = 2


@dataclass
class QgisPlugin:
    """Model describing a QGIS plugin."""

    # optional mapping on attributes names.
    # Structure: {attribute_name_in_output_object: attribute_name_from_input_file}
    ATTR_MAP = {
        "location": "type",
        "qgis_maximum_version": "qgisMaximumVersion",
        "qgis_minimum_version": "qgisMinimumVersion",
    }

    OFFICIAL_REPOSITORY_URL_BASE = "https://plugins.qgis.org/"
    OFFICIAL_REPOSITORY_XML = "https://plugins.qgis.org/plugins/plugins.xml"

    name: str
    folder_name: str = None
    location: QgisPluginLocation = "remote"
    official_repository: bool = None
    plugin_id: int = None
    qgis_maximum_version: str = None
    qgis_minimum_version: str = None
    repository_url_xml: str = None
    url: str = None
    version: str = "latest"

    @classmethod
    def from_dict(cls, input_dict: dict) -> Self:
        """Create object from a JSON file.

        Args:
            input_dict (dict): input dictionary

        Returns:
            Self: instanciated object
        """
        # map attributes names
        for k, v in cls.ATTR_MAP.items():
            if v.lower() in input_dict.keys():
                input_dict[k] = input_dict.pop(v.lower(), None)

        # official repository autodetection
        if input_dict.get("repository_url_xml") == cls.OFFICIAL_REPOSITORY_XML:
            input_dict["official_repository"] = True
        elif input_dict.get("url") and input_dict.get("url").startswith(
            cls.OFFICIAL_REPOSITORY_URL_BASE
        ):
            input_dict["official_repository"] = True
            input_dict["repository_url_xml"] = cls.OFFICIAL_REPOSITORY_XML
        else:
            pass

        # URL auto build
        if input_dict.get("official_repository") is True and not input_dict.get("url"):
            input_dict["url"] = (
                f"{cls.OFFICIAL_REPOSITORY_URL_BASE}"
                f"plugins/{input_dict.get('folder_name') or input_dict.get('name')}/"
                f"version/{input_dict.get('version')}/download/"
            )
            input_dict["repository_url_xml"] = cls.OFFICIAL_REPOSITORY_XML
            input_dict["location"] = "remote"

        # remove keys which are not in object attributes
        attributes_names = [f.name for f in fields(cls)]
        for k in list(input_dict):
            if k not in attributes_names:
                del input_dict[k]

        # return new instance with loaded object
        return cls(
            **input_dict,
        )

    @classmethod
    def from_plugin_folder(cls, input_plugin_folder: Path) -> Self:
        """Create object from a QGIS plugin folder. Must contain a metadata.txt file.

        Args:
            input_plugin_folder (Path): path to the folder containgin a QGIS plugin

        Returns:
            Self: instanciated object
        """
        # check that input path is a folder
        check_path(
            input_path=input_plugin_folder,
            must_exists=True,
            must_be_a_folder=True,
            must_be_a_file=False,
            must_be_readable=True,
        )
        # check if the folder contains a metadata.txt file
        plugin_metadata_txt = input_plugin_folder / "metadata.txt"
        check_path(
            input_path=plugin_metadata_txt,
            must_be_a_file=True,
            must_be_readable=True,
            must_exists=True,
        )

        # read it
        with plugin_metadata_txt.open() as config_file:
            config = configparser.ConfigParser()
            config.read_file(config_file)
        plugin_md_as_dict = {k: v for k, v in config.items(section="general")}

        # add folder name
        plugin_md_as_dict["folder_name"] = input_plugin_folder.name

        return cls.from_dict(plugin_md_as_dict)

    @classmethod
    def from_zip(cls, input_zip_path: Path) -> Self:
        """Create object from a ZIP file.

        Args:
            input_zip_path (Path): filepath of the input zip

        Returns:
            Self: instanciated object
        """
        with zipfile.ZipFile(file=input_zip_path) as zf:
            # find the metadata.txt file
            for i in zf.infolist():
                if not i.is_dir() and i.filename.split("/")[1] == "metadata.txt":
                    break

            # open and read it
            zip_path = zipfile.Path(zf)
            metadata_file = zip_path / i.filename
            plugin_folder_name = metadata_file.parent.name
            with metadata_file.open() as config_file:
                config = configparser.ConfigParser()
                config.read_file(config_file)

        plugin_md_as_dict = {k: v for k, v in config.items(section="general")}

        # add folder name
        plugin_md_as_dict["folder_name"] = plugin_folder_name

        return cls.from_dict(plugin_md_as_dict)

    @property
    def download_url(self) -> str:
        """Try to guess download URL if it's not set during the object init.

        Returns:
            str: download URL
        """
        if self.url:
            return quote(self.url, safe="/:")
        elif self.repository_url_xml and self.folder_name and self.version:
            split_url = urlsplit(self.repository_url_xml)
            new_url = split_url._replace(path=split_url.path.replace("plugins.xml", ""))
            return f"{urlunsplit(new_url)}{self.folder_name}.{self.version}.zip"
        elif self.repository_url_xml and self.name and self.version:
            split_url = urlsplit(self.repository_url_xml)
            new_url = split_url._replace(path=split_url.path.replace("plugins.xml", ""))
            return f"{urlunsplit(new_url)}{self.name}.{self.version}.zip"
        else:
            return None

    @property
    def id_with_version(self) -> str:
        """Unique identifier using plugin_id (if set) and name + version slugified.

        Returns:
            str: plugin identifier meant to be unique per version
        """
        if self.plugin_id:
            return f"{self.plugin_id}_{sluggy(self.name)}_{sluggy(self.version.replace('.', '-'))}"
        else:
            return f"{sluggy(self.name)}_{sluggy(self.version.replace('.', '-'))}"

    @property
    def installation_folder_name(self) -> str:
        """Name of the folder when the plugin is installed into QGIS/profile/python/plugins/. \
            If not clearly specified intot the profile.json, it tries to extract it from \
            the download URL. As final fallback, it returns the slufigied plugin name.

        Returns:
            str: plugin folder name
        """
        if self.folder_name:
            return self.folder_name
        elif self.download_url:
            try:
                folder_name_from_url = urlsplit(self.download_url).path.split("/")[2]
                self.folder_name = folder_name_from_url
                return folder_name_from_url
            except Exception as err:
                logger.error(
                    f"Plugin {self.name} - Determine plugin folder name from download"
                    f"URL failed. Please specify it into profile.json file. Trace: {err}"
                )
                return sluggy(self.name)
        else:
            return sluggy(self.name)

    def is_older_than(self, version_to_compare: Union[str, Self]) -> bool:
        """Determine if the actual object version is older than the given version to \
            compare.

        Args:
            version_to_compare (Union[str, Self]): given version to compare with object version

        Returns:
            bool: True if the given version is newer (more recent)
        """
        if not any([self.version, version_to_compare]):
            logger.error("Object version is not set, so the comparizon is impossible.")
            return None

        # if a plugin is given
        if isinstance(version_to_compare, QgisPlugin):
            # take the opportunity to check the name is the same
            if not self.name == version_to_compare.name:
                logger.warning(
                    "Be careful, the plugin to compare seems to be different: "
                    f"{self.name} != {version_to_compare.name}"
                )
            # store the version string
            version_to_compare = version_to_compare.version

        # load object version as packaging.Version object
        try:
            plugin_version = Version(self.version)
        except InvalidVersion as err:
            logger.error(
                f"Plugin {self.name} uses an incompatible versioning scheme: {self.version}."
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

        logger.debug(f"Comparing versions: {plugin_version} and {version_to_compare}")

        return plugin_version < version_to_compare


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    sample_plugin_complete = {
        "name": "french_locator_filter",
        "version": "1.0.4",
        "url": "https://plugins.qgis.org/plugins/french_locator_filter/version/1.0.4/download/",
        "type": "remote",
    }

    plugin_obj_one: QgisPlugin = QgisPlugin.from_dict(sample_plugin_complete)
    assert plugin_obj_one.url == plugin_obj_one.download_url
    print(plugin_obj_one)

    sample_plugin_minimal = {
        "name": "french_locator_filter",
        "version": "1.0.4",
        "official_repository": True,
    }

    plugin_obj_two = QgisPlugin.from_dict(sample_plugin_minimal)
    print(plugin_obj_two)

    assert plugin_obj_one == plugin_obj_two

    sample_plugin_unofficial = {
        "name": "Geotuileur",
        "version": "1.0.0",
        "official_repository": False,
        "repository_url_xml": "https://oslandia.gitlab.io/qgis/ign-geotuileur/plugins.xml",
    }

    plugin_obj_three: QgisPlugin = QgisPlugin.from_dict(sample_plugin_unofficial)
    print(plugin_obj_three)
    print(plugin_obj_three.folder_name)
    print(plugin_obj_three.installation_folder_name)
    print(plugin_obj_three.download_url)

    sample_plugin_different_name = {
        "name": "Layers menu from project",
        "version": "v2.0.6",
        "url": "https://plugins.qgis.org/plugins/menu_from_project/version/v2.0.6/download/",
        "type": "remote",
        "plugin_id": 1846,
    }

    plugin_obj_four: QgisPlugin = QgisPlugin.from_dict(sample_plugin_different_name)
    print(plugin_obj_four.url)
    print(plugin_obj_four.official_repository)
    print(plugin_obj_four.folder_name)
    print(plugin_obj_four.installation_folder_name)
    print(plugin_obj_four.folder_name)
    assert plugin_obj_four.url == plugin_obj_four.download_url

    sample_zip = (
        Path.home() / ".cache/qgis-deployment-toolbelt/plugins/qompligis_v1-1-0.zip"
    )
    plugin_from_zip: QgisPlugin = QgisPlugin.from_zip(sample_zip)
    print(plugin_from_zip)

    sample_plugin_qtribu = {
        "name": "QTribu",
        "version": "0.14.2",
        "official_repository": True,
        "folder_name": "qtribu",
    }
    plugin_obj_five: QgisPlugin = QgisPlugin.from_dict(sample_plugin_qtribu)
    print(plugin_obj_five.url)

    sample_plugin_qtribu_newer: QgisPlugin = QgisPlugin.from_dict(
        {
            "name": "QTribu",
            "version": "0.15.0",
            "official_repository": True,
            "folder_name": "qtribu",
        }
    )

    assert plugin_obj_five.is_older_than(sample_plugin_qtribu_newer) is True
    assert sample_plugin_qtribu_newer.is_older_than(plugin_obj_five) is False
