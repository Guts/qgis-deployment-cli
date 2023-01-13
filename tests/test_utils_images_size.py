#! python3  # noqa E265

"""
    Usage from the repo root folder:

    .. code-block:: bash
        # for whole tests
        python -m unittest tests.test_utils_images_size
        # for specific test
        python -m unittest tests.test_utils.TestUtilsImagesSizeChecker.get_svg_size
"""


import unittest

# standard library
from pathlib import Path

# project
from qgis_deployment_toolbelt.utils.check_image_size import get_svg_size

# ############################################################################
# ########## Classes #############
# ################################


class TestUtilsImagesSizeChecker(unittest.TestCase):
    """Test package utilities."""

    def test_svg_size_with_dimensions(self):
        """Test svg size retriever."""
        svg_with_dimensions_attributes = Path(
            "tests/fixtures/miscellaneous/sample_with_dimensions_attributes.svg"
        )

        self.assertTrue(svg_with_dimensions_attributes.is_file())
        # svg with dimensions set
        svg_size = get_svg_size(image_filepath=svg_with_dimensions_attributes)

        self.assertIsInstance(svg_size, tuple)
        self.assertIsInstance(svg_size[0], int)
        self.assertIsInstance(svg_size[1], int)
        self.assertEqual(svg_size[0], 853)
        self.assertEqual(svg_size[1], 568)

    def test_svg_size_without_dimensions(self):
        """Test svg size retriever."""
        svg_without_dimensions_attributes = Path(
            "tests/fixtures/miscellaneous/sample_without_dimensions_attributes.svg"
        )

        self.assertTrue(svg_without_dimensions_attributes.is_file())
        # svg with dimensions set
        svg_size = get_svg_size(image_filepath=svg_without_dimensions_attributes)

        self.assertIsNone(svg_size)


# ############################################################################
# ####### Stand-alone run ########
# ################################
if __name__ == "__main__":
    unittest.main()
