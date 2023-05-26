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

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)

# #############################################################################
# ########## Classes ###############
# ##################################


class QgisIniHelper:
    """Helper to manipulate QGIS3.ini and QGISCUSTOMIZATION3.ini files."""

    def __init__(self, qgis3ini_filepath: Path) -> None:
        """Instanciation.

        Args:
            qgis3ini_filepath (Path): path to the QGIS3.ini configuration file
        """
        self.qgis3ini_filepath = qgis3ini_filepath
        self.qgiscustomization3ini_filepath = qgis3ini_filepath.with_name(
            "QGISCUSTOMIZATION3.ini"
        )

    def set_ui_customization_enabled(
        self, section: str, option: str, switch: bool = True
    ) -> bool:
        """Enable/disable UI customization in the profile QGIS3.ini file.

        Args:
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
        if not self.qgis3ini_filepath.exists():
            logger.warning(
                f"Configuration file {self.qgis3ini_filepath} doesn't exist. "
                "It will be created but maybe it was not the expected behavior."
            )
            self.qgis3ini_filepath.touch(exist_ok=True)
            self.qgis3ini_filepath.write_text(
                data=f"[{section}]\n{option}={switch_value}", encoding="UTF8"
            )
            return switch

        # read configuration file
        ini_qgis3 = ConfigParser()
        ini_qgis3.optionxform = str
        ini_qgis3.read(self.qgis3ini_filepath, encoding="UTF8")

        # if section and option already exist
        if ini_qgis3.has_option(section=section, option=option):  # = section AND option
            actual_state = ini_qgis3.getboolean(section=section, option=option)
            # when actual UI customization is enabled
            if actual_state and switch:
                logger.debug(
                    f"UI Customization is already ENABLED in {self.qgis3ini_filepath}"
                )
                return True
            elif actual_state and not switch:
                ini_qgis3.set(
                    section=section,
                    option=option,
                    value=switch_value,
                )
                with self.qgis3ini_filepath.open("w", encoding="UTF8") as configfile:
                    ini_qgis3.write(configfile, space_around_delimiters=False)
                logger.debug(
                    "UI Customization was ENABLED and has been "
                    f"DISABLED in {self.qgis3ini_filepath}"
                )
                return False

            # when actual UI customization is disabled
            elif not actual_state and switch:
                ini_qgis3.set(
                    section=section,
                    option=option,
                    value=switch_value,
                )
                with self.qgis3ini_filepath.open("w", encoding="UTF8") as configfile:
                    ini_qgis3.write(configfile, space_around_delimiters=False)
                logger.debug(
                    "UI Customization was DISABLED and has been "
                    f"ENABLED in {self.qgis3ini_filepath}"
                )
                return True
            elif not actual_state and not switch:
                logger.debug(
                    f"UI Customization is already DISABLED in {self.qgis3ini_filepath}"
                )
                return True
        elif ini_qgis3.has_section(section=section) and switch:
            # section exist but not the option, so let's add it as required
            ini_qgis3.set(
                section=section,
                option=option,
                value=switch_value,
            )
            with self.qgis3ini_filepath.open("w", encoding="UTF8") as configfile:
                ini_qgis3.write(configfile, space_around_delimiters=False)
            logger.debug(
                f"'{option}' option was missing in {section}, it's just been added and "
                f"ENABLED in {self.qgis3ini_filepath}"
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
            with self.qgis3ini_filepath.open("w", encoding="UTF8") as configfile:
                ini_qgis3.write(configfile, space_around_delimiters=False)
            logger.debug(
                f"'{option}' option was missing in {section}, it's just been added and "
                f"ENABLED in {self.qgis3ini_filepath}"
            )
            return True
        else:
            logger.debug(
                f"Section '{section}' is not present so {option} is DISABLED in "
                f"{self.qgis3ini_filepath}"
            )
            return False
