#! python3  # noqa: E265

"""Helpers to format text and variables."""


# #############################################################################
# ########## Libraries #############
# ##################################


# Standard library
import logging
from math import floor
from math import log as math_log

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Functions #############
# ##################################


def convert_octets(octets: int) -> str:
    """Convert a mount of octets in readable size.

    Args:
        octets: mount of octets to convert

    Returns:
        size in a human readable format: ko, Mo, etc.

    Example:

    .. code-block:: python

        >>> convert_octets(1024)
        1 ko
        >>> from pathlib import Path
        >>> convert_octets(Path(my_file.txt).stat().st_size)
    """
    # check zero
    if octets == 0:
        return "0 octet"

    # conversion
    size_name = ("octets", "Ko", "Mo", "Go", "To", "Po")
    i = int(floor(math_log(octets, 1024)))
    p = pow(1024, i)
    s = round(octets / p, 2)

    return f"{s} {size_name[i]}"
