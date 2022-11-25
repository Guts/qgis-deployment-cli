#! python3  # noqa: E265

"""
    Check image size using pure Python <https://github.com/shibukawa/imagesize_py>.

    Author: Julien Moura (https://github.com/guts)
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from os import R_OK, access
from pathlib import Path
from typing import Union

# 3rd party
import imagesize

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)

compatible_images_extensions: tuple = (".jpg", ".jpeg", ".png")

# #############################################################################
# ########## Functions #############
# ##################################


def check_image_dimensions(
    image_filepath: Union[str, Path],
    min_width: int = 500,
    max_width: int = 600,
    min_height: int = 250,
    max_height: int = 350,
) -> bool:
    """Check input image dimensions against passed limits.

    :param Union[str, Path] image_filepath: path to the image to check
    :param int min_width: _description_, defaults to 500
    :param int max_width: _description_, defaults to 600
    :param int min_height: _description_, defaults to 250
    :param int max_height: _description_, defaults to 350

    :return bool: True if image dimensions are inferior

    :example:

    .. code-block:: python

        sample_txt = "Oyé oyé brâves gens de 1973 ! Hé oh ! Sentons-nous l'ail %$*§ ?!"
        print(sluggy(sample_txt))
        > oye-oye-braves-gens-de-1973-he-oh-sentons-nous-lail
    """
    # check input path
    if not isinstance(image_filepath, (str, Path)):
        raise TypeError(
            f"image_filepath must be a string or a Path, not {type(image_filepath)}."
        )

    if isinstance(image_filepath, str):
        try:
            image_filepath = Path(image_filepath)
        except Exception as exc:
            raise TypeError(f"Converting image_filepath into Path failed. Trace: {exc}")

    # check if file exists
    if not image_filepath.exists():
        raise FileExistsError(
            "YAML file to check doesn't exist: {}".format(image_filepath.resolve())
        )

    # check if it's a file
    if not image_filepath.is_file():
        raise IOError("YAML file is not a file: {}".format(image_filepath.resolve()))

    # check if file is readable
    if not access(image_filepath, R_OK):
        raise IOError("yaml file isn't readable: {}".format(image_filepath))

    pass


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
