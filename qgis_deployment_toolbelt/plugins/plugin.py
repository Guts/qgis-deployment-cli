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

    name: str = None
    version: str = "latest"
    location: QgisPluginLocation = "remote"
    url: str = None
    repository_url_xml: str = None
    official_repository: bool = None

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
        else:
            pass

        # URL auto build
        if input_dict.get("official_repository") is True:
            input_dict["url"] = (
                f"{cls.OFFICIAL_REPOSITORY_URL_BASE}/"
                f"plugins/{input_dict.get('name')}/{input_dict.get('version')}/download"
            )
            input_dict["repository_url_xml"] = cls.OFFICIAL_REPOSITORY_XML

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

    plugin_obj_one = QgisPlugin.from_dict(sample_plugin_complete)
    print(plugin_obj_one)

    sample_plugin_incomplete = {
        "name": "french_locator_filter",
        "version": "1.0.4",
        "official_repository": True,
    }

    plugin_obj_two = QgisPlugin.from_dict(sample_plugin_incomplete)
    print(plugin_obj_two)

    assert plugin_obj_one == plugin_obj_two
