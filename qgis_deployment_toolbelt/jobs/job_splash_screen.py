#! python3  # noqa: E265

"""
    Manage application shortcuts on end-user machine.

    Author: Julien Moura (https://github.com/guts)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from configparser import ConfigParser
from pathlib import Path
from sys import platform as opersys

# package
from qgis_deployment_toolbelt.constants import OS_CONFIG
from qgis_deployment_toolbelt.profiles.qdt_profile import QdtProfile

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################


class JobSplashScreenManager:
    """
    Job to set-up splash screen for QGIS profile.
    """

    ID: str = "splash-screen-manager"
    OPTIONS_SCHEMA: dict = {
        "action": {
            "type": str,
            "required": False,
            "default": "create_or_restore",
            "possible_values": ("create", "create_or_restore", "remove"),
            "condition": "in",
        },
        "source_profiles": {
            "type": str,
            "required": False,
            "default": ".cache/qgis-deployment-toolbelt/profiles",
            "possible_values": None,
            "condition": None,
        },
    }
    DEFAULT_SPLASH_FILEPATH: str = "images/splash.png"
    SPLASH_FILENAME: str = "splash.png"

    def __init__(self, options: dict) -> None:
        """Instantiate the class.

        :param dict options: profiles source (remote, can be a local network) and
        destination (local).
        """
        self.options: dict = self.validate_options(options)

        # profile folder
        if opersys not in OS_CONFIG:
            raise OSError(
                f"Your operating system {opersys} is not supported. "
                f"Supported platforms: {','.join(OS_CONFIG.keys())}."
            )
        self.qgis_profiles_path: Path = Path(OS_CONFIG.get(opersys).profiles_path)
        if not self.qgis_profiles_path.exists():
            logger.warning(
                f"QGIS profiles folder not found: {self.qgis_profiles_path}. "
                "Creating it to properly run the job."
            )
            self.qgis_profiles_path.mkdir(parents=True)

    def run(self) -> None:
        """Execute job logic."""
        li_installed_profiles_path = [
            d
            for d in self.qgis_profiles_path.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        ]

        if self.options.get("action") in ("create", "create_or_restore"):
            for profile_dir in li_installed_profiles_path:

                # default absolute splash screen path
                splash_screen_filepath = profile_dir / self.DEFAULT_SPLASH_FILEPATH

                # target QGIS configuration files
                cfg_qgis_base = profile_dir / "QGIS/QGIS3.ini"
                cfg_qgis_custom = profile_dir / "QGIS/QGISCUSTOMIZATION3.ini"

                # case where splash image is specified into the profile.json
                if Path(profile_dir / "profile.json").is_file():
                    qdt_profile = QdtProfile.from_json(
                        profile_json_path=Path(profile_dir / "profile.json"),
                        profile_folder=profile_dir.resolve(),
                    )

                    # if the splash image referenced into the profile.json exists, make
                    # sure it complies QGIS splash screen rules
                    if (
                        isinstance(qdt_profile.splash, Path)
                        and qdt_profile.splash.is_file()
                    ):
                        # make sure that the filename complies with what QGIS expects
                        if qdt_profile.splash.name != splash_screen_filepath.name:
                            splash_filepath = qdt_profile.splash.with_name(
                                self.SPLASH_FILENAME
                            )
                            qdt_profile.splash.replace(splash_filepath)
                            logger.debug(
                                f"Specified splash screen renamed into {splash_filepath}."
                            )
                        else:
                            # homogeneize filepath var name
                            logger.debug(
                                f"Splash screen already exists at {splash_screen_filepath}"
                            )

                # now, splash screen image should be at {profile_dir}/images/splash.png
                if not splash_screen_filepath.is_file():
                    # TODO: check image size to fit QGIS restrictions
                    logger.debug(
                        f"No splash screen found or defined for profile {profile_dir.name}"
                    )
                    continue

                # enable UI customization
                self.set_ui_customization_enabled(
                    qgis3ini_filepath=cfg_qgis_base,
                    section="UI",
                    option="Customization\\enabled",
                    switch=True,
                )

                # set the splash screen into the customization file

        else:
            raise NotImplementedError

        logger.debug(f"Job {self.ID} ran successfully.")

    # -- INTERNAL LOGIC ------------------------------------------------------
    def set_ui_customization_enabled(
        self, qgis3ini_filepath: Path, section: str, option: str, switch: bool = True
    ) -> bool:
        """Enable/disable UI customization in the profile QGIS3.ini file.

        :param Path qgis3ini_filepath: path to the QGIS3.ini configuration file
        :param str section: section name in ini file
        :param str option: option name in the section of the ini file
        :param bool switch: True to enable, False to disable UI customization,
        defaults to True

        :return bool: UI customization state. True is enabled, False is disabled.
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

        # check
        ini_qgis3 = ConfigParser()
        ini_qgis3.optionxform = str
        ini_qgis3.read(qgis3ini_filepath, encoding="UTF8")

        if ini_qgis3.has_option(section=section, option=option):
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

    def apply_custom(
        self, profile_customization_filepath: Path, splash_screen_folder_path: Path
    ):
        """Apply custom splash screen."""
        # modify splash path
        if profile_customization_filepath.exists():
            ini_custom = ConfigParser()
            ini_custom.optionxform = str
            ini_custom.read(profile_customization_filepath, encoding="UTF8")

            if "Customization" in ini_custom.sections():
                ini_custom.set(
                    section="Customization",
                    option="splashpath",
                    value=splash_screen_folder_path,
                )
                with profile_customization_filepath.open(
                    "w", encoding="UTF8"
                ) as configfile:
                    ini_custom.write(configfile, space_around_delimiters=False)

        else:
            ini_custom = ConfigParser()
            ini_custom["Customization"] = {"splashpath": splash_screen_folder_path}
            with profile_customization_filepath.open(
                mode="w", encoding="UTF8"
            ) as configfile:
                ini_custom.write(configfile, space_around_delimiters=False)

            self.log(
                message="Customization file did not exists. "
                f"It has been created with the new splash screen: {profile_customization_filepath}"
            )

    def validate_options(self, options: dict) -> bool:
        """Validate options.

        :param dict options: options to validate.
        :return bool: True if options are valid.
        """
        for option in options:
            if option not in self.OPTIONS_SCHEMA:
                raise Exception(
                    f"Job: {self.ID}. Option '{option}' is not valid."
                    f" Valid options are: {self.OPTIONS_SCHEMA.keys()}"
                )

            option_in = options.get(option)
            option_def: dict = self.OPTIONS_SCHEMA.get(option)
            # check value type
            if not isinstance(option_in, option_def.get("type")):
                raise Exception(
                    f"Job: {self.ID}. Option '{option}' has an invalid value."
                    f"\nExpected {option_def.get('type')}, got {type(option_in)}"
                )
            # check value condition
            if option_def.get("condition") == "startswith" and not option_in.startswith(
                option_def.get("possible_values")
            ):
                raise Exception(
                    f"Job: {self.ID}. Option '{option}' has an invalid value."
                    "\nExpected: starts with one of: "
                    f"{', '.join(option_def.get('possible_values'))}"
                )
            elif option_def.get(
                "condition"
            ) == "in" and option_in not in option_def.get("possible_values"):
                raise Exception(
                    f"Job: {self.ID}. Option '{option}' has an invalid value."
                    f"\nExpected: one of: {', '.join(option_def.get('possible_values'))}"
                )
            else:
                pass

        return options


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
