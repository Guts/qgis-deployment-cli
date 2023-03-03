#! python3  # noqa E265

"""Usage from the repo root folder:

    .. code-block:: python

        # for whole test
        python -m unittest tests.test_job_generic
        # for specific
        python -m unittest tests.test_job_generic.TestJobGeneric.test_validate_options
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import unittest

from qgis_deployment_toolbelt.exceptions import (
    JobOptionBadName,
    JobOptionBadValue,
    JobOptionBadValueType,
)

# package
from qgis_deployment_toolbelt.jobs.generic_job import GenericJob

# #############################################################################
# ########## Classes ###############
# ##################################


class TestJobGeneric(unittest.TestCase):
    """Test generic job."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        cls.generic_job = GenericJob()

        cls.generic_job.ID = "job-test-fixture"
        cls.generic_job.OPTIONS_SCHEMA = {
            "option_one": {
                "type": str,
                "required": True,
                "default": "git",
                "condition": "startswith",
                "possible_values": ("git", "http"),
            },
            "option_two": {
                "type": (bool, int, str),
                "required": False,
                "condition": "in",
                "possible_values": ("test", "fixture"),
            },
            "option_three": {
                "type": (bool, int, str),
                "required": False,
                "condition": None,
                "possible_values": None,
            },
        }

    # -- TESTS ---------------------------------------------------------
    def test_validate_options_bad_input_type(self):
        """Test validate_options method"""

        # Options must be a dictionary
        with self.assertRaises(TypeError):
            self.generic_job.validate_options(options="options_test")
        with self.assertRaises(TypeError):
            self.generic_job.validate_options(options=["options_test"])

    def test_validate_options_bad_name(self):
        """Test validate_options method"""
        # bad option name
        bad_option_name = {
            "option_one": "http://fake.url",
            "option_two": "test",
            "bad_option_name": "git",
        }

        with self.assertRaises(JobOptionBadName):
            self.generic_job.validate_options(bad_option_name)

    def test_validate_options_bad_condition_in(self):
        """Test validate_options method"""
        # bad value condition
        bad_options_scope = {
            "option_one": "https://fake.url",
            "option_two": "bad-value-not-in-possibles",
        }

        with self.assertRaises(JobOptionBadValue):
            self.generic_job.validate_options(bad_options_scope)

    def test_validate_options_bad_condition_startswith(self):
        """Test validate_options method"""
        # bad value condition
        bad_options_scope = {
            "option_one": "bad-startswith",
            "option_two": "user",
        }

        with self.assertRaises(JobOptionBadValue):
            self.generic_job.validate_options(bad_options_scope)

    def test_validate_options_bad_type(self):
        """Test validate_options method"""
        # bad value type
        bad_options = {
            "option_one": True,
            "option_two": "user",
        }

        with self.assertRaises(JobOptionBadValueType):
            self.generic_job.validate_options(bad_options)
