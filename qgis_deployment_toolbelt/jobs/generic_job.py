#! python3  # noqa: E265

"""
    Base of job.

    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging

# package
from qgis_deployment_toolbelt.exceptions import (
    JobOptionBadName,
    JobOptionBadValue,
    JobOptionBadValueType,
)

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)

# #############################################################################
# ########## Classes ###############
# ##################################


class GenericJob:
    """Generic base for QDT jobs."""

    ID = ""
    OPTIONS_SCHEMA = dict[dict]

    def validate_options(self, options: dict[dict]) -> dict[dict]:
        """Validate options.

        Args:
            options (dict[dict]): options to validate.

        Raises:
            ValueError: if option has an invalid name or doesn't comply with condition
            TypeError: if the option does'nt not comply with expected type

        Returns:
            dict[dict]: options if valid
        """
        if not isinstance(options, dict):
            raise TypeError(f"Options to validate must be a dict, not {type(options)}.")

        for option in options:
            if option not in self.OPTIONS_SCHEMA:
                raise JobOptionBadName(
                    job_id=self.ID,
                    bad_option_name=option,
                    expected_options_names=self.OPTIONS_SCHEMA.keys(),
                )

            option_in = options.get(option)
            option_def: dict = self.OPTIONS_SCHEMA.get(option)
            # check value type
            if not isinstance(option_in, option_def.get("type")):
                raise JobOptionBadValueType(
                    job_id=self.ID,
                    bad_option_name=option,
                    bad_option_value=option_in,
                    expected_option_type=option_def.get("type"),
                )
            # check value condition
            if option_def.get("condition") == "startswith" and not option_in.startswith(
                option_def.get("possible_values")
            ):
                raise JobOptionBadValue(
                    job_id=self.ID,
                    bad_option_name=option,
                    bad_option_value=option_in,
                    condition="startswith",
                    accepted_values=option_def.get("possible_values"),
                )
            elif option_def.get(
                "condition"
            ) == "in" and option_in not in option_def.get("possible_values"):
                raise JobOptionBadValue(
                    job_id=self.ID,
                    bad_option_name=option,
                    bad_option_value=option_in,
                    condition="startswith",
                    accepted_values=option_def.get("possible_values"),
                )
            else:
                pass

        return options
