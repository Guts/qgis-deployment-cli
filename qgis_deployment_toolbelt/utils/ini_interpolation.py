#! python3  # noqa: E265

"""
    Custom INI files interpolation.

    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from collections import ChainMap
from configparser import BasicInterpolation, ConfigParser
from os.path import expanduser, expandvars

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)

# #############################################################################
# ########## Classes ###############
# ##################################


class EnvironmentVariablesInterpolation(BasicInterpolation):
    """Custom interpolation to handle environment variables in ini files.

    Inspired from https://gist.github.com/malexer/ee2f93b1973120925e8beb3f36b184b8.


    Example:

        .. code-block:: ini

            [test]
            user = $USER
            user_home = $HOME
            fake_value_from_environment_variable = $QDT_TEST_ENV_VARIABLE
            pictures = %(user_home)s/.cache/qgis-deployment-toolbelt
    """

    def before_get(
        self,
        parser: ConfigParser,
        section: str,
        option: str,
        value: str,
        defaults: ChainMap,
    ) -> str:
        """Called for every option=value line in INI file.

        Args:
            parser (ConfigParser): parser whose function is overloaded
            section (str): section's name
            option (str): option's name
            value (str): value to try to interpolate
            defaults (ChainMap): defaults options/values

        Returns:
            str: interpolated value
        """
        value = super().before_get(parser, section, option, value, defaults)
        try:
            return expandvars(expanduser(value))
        except Exception as exc:
            logger.error(
                f"Failed to interpolate {value} in {section}/{option}. Trace: {exc}"
            )
            return value


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
