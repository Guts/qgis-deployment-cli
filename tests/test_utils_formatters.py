#! python3  # noqa E265

"""
    Usage from the repo root folder:

    .. code-block:: bash
        # for whole tests
        python -m unittest tests.test_utils_formatters
        # for specific test
        python -m unittest tests.test_utils_formatters.TestUtilsFormatters.test_convert_octets
"""

# standard library
import unittest

# project
from qgis_deployment_toolbelt.utils.formatters import convert_octets

# ############################################################################
# ########## Classes #############
# ################################


class TestUtilsFormatters(unittest.TestCase):
    """Test package utilities."""

    def test_convert_octets(self):
        """Test file size formatter."""
        self.assertEqual(
            convert_octets(1024),
            "1.0 Ko",
        )

        self.assertEqual(
            convert_octets(2097152),
            "2.0 Mo",
        )


# ############################################################################
# ####### Stand-alone run ########
# ################################
if __name__ == "__main__":
    unittest.main()
