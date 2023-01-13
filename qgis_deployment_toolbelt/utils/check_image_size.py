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
import xml.etree.ElementTree as ET
from decimal import Decimal
from pathlib import Path
from typing import Tuple, Union

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


def get_svg_size(image_filepath: Path) -> Tuple[int, int]:
    """Extract SVG width and height from a SVG file and convert them into integers. \
    Relevant and working only if the file root has width and height attributes.

    :param Path image_filepath: path to the svg file

    :return Tuple[int, int]: tuple of dimensions as integers (width,height)
    """
    try:
        tree = ET.parse(image_filepath)
        root = tree.getroot()
    except Exception as err:
        logger.error(f"Unable to open SVG file as XML: {image_filepath}. Trace: {err}")
        return None

    try:
        return (int(Decimal(root.attrib["width"])), int(Decimal(root.attrib["height"])))
    except Exception as err:
        logger.warning(
            "Unable to determine image dimensions from width/height "
            f"attributes: {image_filepath}. It migh be infinitely scalable. Trace: {err}"
        )
        return None


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

    if image_filepath.suffix not in compatible_images_extensions:
        logger.error("Image extension is not supported: ")
        return None
    # print(file.name, file.parents[0])

    # get image dimensions
    try:
        width, height = imagesize.get(image_filepath)
    except ValueError as exc:
        logging.error(f"Invalid image: {image_filepath.resolve()}. Trace: {exc}")
        width, height = -1, -1
    except Exception as exc:
        logging.error(
            f"Something went wrong reading the image: {image_filepath.resolve()}. Trace: {exc}"
        )
        width, height = -1, -1


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    svg_path = Path(
        "tests/fixtures/miscellaneous/sample_with_dimensions_attributes.svg"
    )
    assert svg_path.is_file()
    print(get_svg_size(image_filepath=svg_path))

    svg_path = Path(
        "tests/fixtures/miscellaneous/sample_without_dimensions_attributes.svg"
    )
    assert svg_path.is_file()
    print(get_svg_size(image_filepath=svg_path))
