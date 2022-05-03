#! python3  # noqa: E265

"""
    Tools to manage the environment setup (variables, etc.)

    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from sys import platform as opersys

# Imports depending on operating system
import dulwich

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################


class JobProfilesDownloader:
    """
    Job to download remote profiles and set them.
    """

    ID: str = "qprofiles-manager"

    def __init__(self, options: dict) -> None:
        """Instantiate the class.

        :param dict options: profiles source (remote, can be a local network) and
        destination (local).
        """
        self.options: dict = options

    def run(self) -> None:
        """Apply environment variables from dictionary to the

        :param dict env_vars: dictionary with environment variable name as key and
        some parameters as values (value, scope, action...).
        """
        pass

    def validate_options(self, options: dict) -> bool:
        """Validate options.

        :param dict options: options to validate.
        :return bool: True if options are valid.
        """
        return True


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
