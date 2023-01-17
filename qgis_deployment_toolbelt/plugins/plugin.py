#! python3  # noqa: E265

"""
    Plugin object model.

    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from dataclasses import dataclass
from enum import Enum
from sys import version_info
from urllib.parse import quote, urlsplit, urlunsplit

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
    # {attribute_name_in_output_object: attribute_name_from_input_file}
    ATTR_MAP = {
        "location": "type",
    }

    OFFICIAL_REPOSITORY_URL_BASE = "https://plugins.qgis.org/"
    OFFICIAL_REPOSITORY_XML = "https://plugins.qgis.org/plugins/plugins.xml"

    name: str
    location: QgisPluginLocation = "remote"
    official_repository: bool = None
    plugin_id: int = None
    repository_url_xml: str = None
    url: str = None
    version: str = "latest"

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
    def download_url(self) -> str:
        """Try to guess download URL if it's not set during the object init.

        Returns:
            str: download URL
        """
        if self.url:
            return quote(self.url, safe="/:")
        elif self.repository_url_xml and self.name and self.version:
            split_url = urlsplit(self.repository_url_xml)
            new_url = split_url._replace(path=split_url.path.replace("plugins.xml", ""))
            return f"{urlunsplit(new_url)}{self.name}.{self.version}.zip"
        else:
            return None

    @classmethod
    def from_dict(cls, input_dict: dict) -> Self:
        # map attributes names
        for k, v in cls.ATTR_MAP.items():
            if v in input_dict.keys():
                input_dict[k] = input_dict.pop(v, None)

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
                f"plugins/{input_dict.get('name')}/"
                f"version/{input_dict.get('version')}/download/"
            )
            input_dict["repository_url_xml"] = cls.OFFICIAL_REPOSITORY_XML
            input_dict["location"] = "remote"

        # return new instance with loaded object
        return cls(
            **input_dict,
        )


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

    plugin_obj_three = QgisPlugin.from_dict(sample_plugin_unofficial)
    print(plugin_obj_three)

    sample_plugin_different_name = {
        "name": "Layers menu from project",
        "version": "v2.0.6",
        "url": "https://plugins.qgis.org/plugins/menu_from_project/version/v2.0.6/download/",
        "type": "remote",
    }

    plugin_obj_four: QgisPlugin = QgisPlugin.from_dict(sample_plugin_different_name)
    print(plugin_obj_four.url)
    assert plugin_obj_four.url == plugin_obj_four.download_url
