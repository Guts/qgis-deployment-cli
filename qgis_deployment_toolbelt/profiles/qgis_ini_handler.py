#! python3  # noqa: E265

"""
    Read and write QGIS configuration files.

    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from configparser import ConfigParser
from pathlib import Path
from typing import Literal

# package
from qgis_deployment_toolbelt.utils.ini_interpolation import (
    EnvironmentVariablesInterpolation,
)

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)

# #############################################################################
# ########## Classes ###############
# ##################################


class QgisIniHelper:
    """Helper to manipulate QGIS configuration files (*.ini)."""

    INI_TYPE: Literal["profile_qgis3", "profile_qgis3customization"] = None

    def __init__(
        self,
        ini_filepath: Path,
        strict: bool = False,
        enable_environment_variables_interpolation: bool = True,
    ) -> None:
        """Instanciation.

        Args:
            ini_filepath: path to the QGIS3.ini configuration file
        """
        if ini_filepath.stem == "QGIS3":
            self.INI_TYPE = "profile_qgis3"
            self.profile_config_path = ini_filepath
            self.profile_customization_path = ini_filepath.with_name(
                "QGISCUSTOMIZATION3.ini"
            )
        elif ini_filepath.stem == "QGISCUSTOMIZATION3":
            self.INI_TYPE = "profile_qgis3customization"
            self.profile_config_path = ini_filepath.with_name("QGIS3.ini")
            self.profile_customization_path = ini_filepath
        else:
            logger.warning(f"Unrecognized ini type: {ini_filepath}")

        # store options
        self.strict_mode = strict
        self.enable_environment_variables_interpolation = (
            enable_environment_variables_interpolation
        )

    def cfg_parser(self) -> ConfigParser:
        """Return config parser with options for QGIS ini files.

        Returns:
            ConfigParser: config parser
        """
        qgis_cfg_parser = ConfigParser(
            strict=self.strict_mode,
            interpolation=EnvironmentVariablesInterpolation()
            if self.enable_environment_variables_interpolation
            else None,
        )
        qgis_cfg_parser.optionxform = str
        return qgis_cfg_parser

    # UI customization
    def is_ui_customization_enabled(self, ini_file: ConfigParser | Path = None) -> bool:
        """Determine if UI customization is enabled.

        Args:
            ini_file (Union[ConfigParser, Path]): input ini file to check.
                A warning is raised if the filename is not QGIS3.ini.
                If None, self.profile_config_path is used.

        Returns:
            bool: True if customization is enabled
        """

        if isinstance(ini_file, ConfigParser):
            if ini_file.has_option(section="UI", option="Customization\\enabled"):
                return ini_file.getboolean(
                    section="UI", option="Customization\\enabled"
                )
            else:
                return False
        elif isinstance(ini_file, Path):
            if ini_file.stem == "QGIS3":
                logger.warning(
                    "Input file does not seem to be a QGIS profile configuration file "
                    f"(QGIS/QGIS3.ini): {ini_file}"
                )

            cfg_parser = self.cfg_parser()
            cfg_parser.read(ini_file, encoding="UTF8")
            return self.is_ui_customization_enabled(cfg_parser)
        elif ini_file is None and self.profile_config_path.exists():
            cfg_parser = self.cfg_parser()
            cfg_parser.read(self.profile_config_path, encoding="UTF8")
            return self.is_ui_customization_enabled(cfg_parser)

    def set_ui_customization_enabled(self, switch: bool = True) -> bool:
        """Enable/disable UI customization in the profile QGIS3.ini file.

        Args:
            switch (bool, optional): True to enable, False to disable UI customization.
                Defaults to True.

        Returns:
            bool: UI customization state. True is enabled, False is disabled.
        """
        # local variables
        section = "UI"
        option = "Customization\\enabled"

        # boolean syntax for PyQt
        switch_value = "false"
        if switch:
            switch_value = "true"

        # make sure that the file exists
        if not self.profile_config_path.exists():
            logger.warning(
                f"Configuration file {self.profile_config_path} doesn't exist. "
                "It will be created but maybe it was not the expected behavior."
            )
            self.profile_config_path.touch(exist_ok=True)
            self.profile_config_path.write_text(
                data=f"[UI]\nCustomization\\enabled={switch_value}", encoding="UTF8"
            )
            return switch

        # read configuration file
        ini_qgis3 = self.cfg_parser()
        ini_qgis3.read(self.profile_config_path, encoding="UTF8")

        # if section and option already exist
        if ini_qgis3.has_option(section=section, option=option):  # = section AND option
            actual_state = ini_qgis3.getboolean(section=section, option=option)
            # when actual UI customization is enabled
            if actual_state and switch:
                logger.debug(
                    f"UI Customization is already ENABLED in {self.profile_config_path}"
                )
                return True
            elif actual_state and not switch:
                ini_qgis3.set(
                    section=section,
                    option=option,
                    value=switch_value,
                )
                with self.profile_config_path.open("w", encoding="UTF8") as configfile:
                    ini_qgis3.write(configfile, space_around_delimiters=False)
                logger.debug(
                    "UI Customization was ENABLED and has been "
                    f"DISABLED in {self.profile_config_path}"
                )
                return False

            # when actual UI customization is disabled
            elif not actual_state and switch:
                ini_qgis3.set(
                    section=section,
                    option=option,
                    value=switch_value,
                )
                with self.profile_config_path.open("w", encoding="UTF8") as configfile:
                    ini_qgis3.write(configfile, space_around_delimiters=False)
                logger.debug(
                    "UI Customization was DISABLED and has been "
                    f"ENABLED in {self.profile_config_path}"
                )
                return True
            elif not actual_state and not switch:
                logger.debug(
                    f"UI Customization is already DISABLED in {self.profile_config_path}"
                )
                return True
        elif ini_qgis3.has_section(section=section) and switch:
            # section exist but not the option, so let's add it as required
            ini_qgis3.set(
                section=section,
                option=option,
                value=switch_value,
            )
            with self.profile_config_path.open("w", encoding="UTF8") as configfile:
                ini_qgis3.write(configfile, space_around_delimiters=False)
            logger.debug(
                f"'{option}' option was missing in {section}, it's just been added and "
                f"ENABLED in {self.profile_config_path}"
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
            with self.profile_config_path.open("w", encoding="UTF8") as configfile:
                ini_qgis3.write(configfile, space_around_delimiters=False)
            logger.debug(
                f"'{option}' option was missing in {section}, it's just been added and "
                f"ENABLED in {self.profile_config_path}"
            )
            return True
        else:
            logger.debug(
                f"Section '{section}' is not present so {option} is DISABLED in "
                f"{self.profile_config_path}"
            )
            return False


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    new_config_file = Path("tests/fixtures/qgis_ini/default_no_customization/QGIS3.ini")
    assert new_config_file.exists()
    ini_config = QgisIniHelper(ini_filepath=new_config_file)

    print(ini_config.is_ui_customization_enabled())
