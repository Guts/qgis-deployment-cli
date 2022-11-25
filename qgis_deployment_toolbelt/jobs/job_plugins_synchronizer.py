#! python3  # noqa: E265

"""
    Manage plugins listed into profiles.

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


class JobPluginsManager:
    """
    Job to download and synchronize plugins.
    """

    ID: str = "plugins-manager"
    OPTIONS_SCHEMA: dict = {
        "action": {
            "type": str,
            "required": False,
            "default": "create_or_restore",
            "possible_values": ("create", "create_or_restore", "remove"),
            "condition": "in",
        }
    }

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
                else:
                    logger.debug(f"No profile.json found for profile '{profile_dir}")

                # now, splash screen image should be at {profile_dir}/images/splash.png
                if not splash_screen_filepath.is_file():
                    # TODO: check image size to fit QGIS restrictions
                    logger.debug(
                        f"No splash screen found or defined for profile {profile_dir.name}"
                    )
                    continue
        else:
            raise NotImplementedError

        logger.debug(f"Job {self.ID} ran successfully.")

    # -- INTERNAL LOGIC ------------------------------------------------------
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
