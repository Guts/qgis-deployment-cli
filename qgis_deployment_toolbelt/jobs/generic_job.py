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
from configparser import ConfigParser
from pathlib import Path

# package
from qgis_deployment_toolbelt.exceptions import (
    JobOptionBadName,
    JobOptionBadValue,
    JobOptionBadValueType,
)
from qgis_deployment_toolbelt.profiles.qdt_profile import QdtProfile

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

    def filter_profiles_folder(self) -> tuple[QdtProfile]:
        """Parse downloaded folder to filter on QGIS profiles folders.

        Returns:
            tuple[QdtProfile]: tuple of profiles objects
        """
        # first, try to get folders containing a profile.json
        qgis_profiles_folder = [
            QdtProfile.from_json(profile_json_path=f, profile_folder=f.parent)
            for f in self.qdt_working_folder.glob("**/profile.json")
        ]
        if len(qgis_profiles_folder):
            logger.debug(
                f"{len(qgis_profiles_folder)} profiles found within {self.qdt_working_folder}"
            )
            return tuple(qgis_profiles_folder)

        # if empty, try to identify if a folder is a QGIS profile - but unsure
        for d in self.qdt_working_folder.glob("**"):
            if (
                d.is_dir()
                and d.parent.name == "profiles"
                and not d.name.startswith(".")
            ):
                qgis_profiles_folder.append(QdtProfile(folder=d, name=d.name))

        if len(qgis_profiles_folder):
            return tuple(qgis_profiles_folder)

        # if still empty, raise a warning but returns every folder under a `profiles` folder
        # TODO: try to identify if a folder is a QGIS profile with some approximate criteria

        if not len(qgis_profiles_folder):
            logger.error("No QGIS profile found in the downloaded folder.")
            return None

    def set_ui_customization_enabled(
        self, qgis3ini_filepath: Path, section: str, option: str, switch: bool = True
    ) -> bool:
        """Enable/disable UI customization in the profile QGIS3.ini file.

        Args:
            qgis3ini_filepath (Path): path to the QGIS3.ini configuration file
            section (str): section name in ini file
            option (str): option name in the section of the ini file
            switch (bool, optional): True to enable, False to disable UI customization.
                Defaults to True.

        Returns:
            bool: UI customization state. True is enabled, False is disabled.
        """
        # boolean syntax for PyQt
        switch_value = "false"
        if switch:
            switch_value = "true"

        # make sure that the file exists
        if not qgis3ini_filepath.exists():
            logger.warning(
                f"Configuration file {qgis3ini_filepath} doesn't exist. "
                "It will be created but maybe it was not the expected behavior."
            )
            qgis3ini_filepath.touch(exist_ok=True)
            qgis3ini_filepath.write_text(
                data=f"[{section}]\n{option}={switch_value}", encoding="UTF8"
            )
            return switch

        # read configuration file
        ini_qgis3 = ConfigParser()
        ini_qgis3.optionxform = str
        ini_qgis3.read(qgis3ini_filepath, encoding="UTF8")

        # if section and option already exist
        if ini_qgis3.has_option(section=section, option=option):  # = section AND option
            actual_state = ini_qgis3.getboolean(section=section, option=option)
            # when actual UI customization is enabled
            if actual_state and switch:
                logger.debug(
                    f"UI Customization is already ENABLED in {qgis3ini_filepath}"
                )
                return True
            elif actual_state and not switch:
                ini_qgis3.set(
                    section=section,
                    option=option,
                    value=switch_value,
                )
                with qgis3ini_filepath.open("w", encoding="UTF8") as configfile:
                    ini_qgis3.write(configfile, space_around_delimiters=False)
                logger.debug(
                    "UI Customization was ENABLED and has been "
                    f"DISABLED in {qgis3ini_filepath}"
                )
                return False

            # when actual UI customization is disabled
            elif not actual_state and switch:
                ini_qgis3.set(
                    section=section,
                    option=option,
                    value=switch_value,
                )
                with qgis3ini_filepath.open("w", encoding="UTF8") as configfile:
                    ini_qgis3.write(configfile, space_around_delimiters=False)
                logger.debug(
                    "UI Customization was DISABLED and has been "
                    f"ENABLED in {qgis3ini_filepath}"
                )
                return True
            elif not actual_state and not switch:
                logger.debug(
                    f"UI Customization is already DISABLED in {qgis3ini_filepath}"
                )
                return True
        elif ini_qgis3.has_section(section=section) and switch:
            # section exist but not the option, so let's add it as required
            ini_qgis3.set(
                section=section,
                option=option,
                value=switch_value,
            )
            with qgis3ini_filepath.open("w", encoding="UTF8") as configfile:
                ini_qgis3.write(configfile, space_around_delimiters=False)
            logger.debug(
                f"'{option}' option was missing in {section}, it's just been added and "
                f"ENABLED in {qgis3ini_filepath}"
            )
            return True
        elif not ini_qgis3.has_section(section=section) and switch:
            # even the section is missing. Let's add everything
            ini_qgis3.add_section(section)
            ini_qgis3.set(
                section=section,
                option=option,
                value=switch_value,
            )
            with qgis3ini_filepath.open("w", encoding="UTF8") as configfile:
                ini_qgis3.write(configfile, space_around_delimiters=False)
            logger.debug(
                f"'{option}' option was missing in {section}, it's just been added and "
                f"ENABLED in {qgis3ini_filepath}"
            )
            return True
        else:
            logger.debug(
                f"Section '{section}' is not present so {option} is DISABLED in {qgis3ini_filepath}"
            )
            return False

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
