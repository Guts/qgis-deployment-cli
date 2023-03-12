#! python3  # noqa: E265

"""
    Manage splash screens for QGIS Profiles.

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
from qgis_deployment_toolbelt.constants import OS_CONFIG, get_qdt_working_directory
from qgis_deployment_toolbelt.exceptions import SplashScreenBadDimensions
from qgis_deployment_toolbelt.jobs.generic_job import GenericJob
from qgis_deployment_toolbelt.profiles.qdt_profile import QdtProfile
from qgis_deployment_toolbelt.utils.check_image_size import check_image_dimensions
from qgis_deployment_toolbelt.utils.win32utils import normalize_path

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################


class JobSplashScreenManager(GenericJob):
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
        "strict": {
            "type": bool,
            "required": False,
            "default": False,
            "possible_values": None,
            "condition": None,
        },
    }
    DEFAULT_SPLASH_FILEPATH: str = "images/splash.png"
    SPLASH_FILENAME: str = "splash.png"

    def __init__(self, options: dict) -> None:
        """Instantiate the class.

        Args:
            options (dict): dictionary of options.
        """
        self.options: dict = self.validate_options(options)

        # profile folder
        self.qdt_working_folder = get_qdt_working_directory()
        self.qgis_profiles_path: Path = Path(OS_CONFIG.get(opersys).profiles_path)
        if not self.qgis_profiles_path.exists():
            logger.warning(
                f"QGIS profiles folder not found: {self.qgis_profiles_path}. "
                "Creating it to properly run the job."
            )
            self.qgis_profiles_path.mkdir(parents=True)

    def run(self) -> None:
        """Execute job logic."""
        # check of there are some profiles folders within the downloaded folder
        downloaded_profiles = self.filter_profiles_folder()
        if downloaded_profiles is None:
            logger.error("No QGIS profile found in the downloaded folder.")
            return

        li_installed_profiles_path = [
            d
            for d in self.qgis_profiles_path.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        ]

        if self.options.get("action") in ("create", "create_or_restore"):
            for profile_downloaded in downloaded_profiles:
                # default absolute splash screen path
                splash_screen_filepath = (
                    profile_downloaded.path_in_qgis / self.DEFAULT_SPLASH_FILEPATH
                )
                # target QGIS configuration files
                cfg_qgis_base = profile_downloaded.path_in_qgis / "QGIS/QGIS3.ini"
                cfg_qgis_custom = (
                    profile_downloaded.path_in_qgis / "QGIS/QGISCUSTOMIZATION3.ini"
                )

                if Path(profile_downloaded.path_in_qgis, "profile.json").is_file():
                    profile_installed: QdtProfile = QdtProfile.from_json(
                        profile_json_path=Path(
                            profile_downloaded.path_in_qgis, "profile.json"
                        ),
                        profile_folder=profile_downloaded.path_in_qgis,
                    )

                    # if the splash image referenced into the profile.json exists, make
                    # sure it complies QGIS splash screen rules
                    if (
                        isinstance(profile_installed.splash, Path)
                        and profile_installed.splash.is_file()
                    ):
                        # make sure that the filename complies with what QGIS expects
                        if profile_installed.splash.name != splash_screen_filepath.name:
                            splash_filepath = profile_installed.splash.with_name(
                                self.SPLASH_FILENAME
                            )
                            profile_installed.splash.replace(splash_filepath)
                            logger.debug(
                                f"Specified splash screen renamed into {splash_filepath}."
                            )
                        else:
                            # homogeneize filepath var name
                            logger.debug(
                                f"Splash screen already exists at {splash_screen_filepath}"
                            )

                else:
                    logger.debug(
                        f"No profile.json found for profile '{profile_installed.folder}"
                    )

                # now, splash screen image should be at {profile_dir}/images/splash.png
                if not splash_screen_filepath.is_file():
                    logger.debug(
                        f"No splash screen found or defined for profile: {profile_installed.name}"
                    )
                    continue

                # check image size to fit QGIS restrictions
                is_img_compliant = check_image_dimensions(
                    image_filepath=splash_screen_filepath.resolve(),
                    max_width=605,
                    max_height=305,
                    allowed_images_extensions=(".png",),
                )
                if not is_img_compliant:
                    err = SplashScreenBadDimensions(
                        image_filepath=splash_screen_filepath,
                        profile_name=profile_installed.name,
                    )
                    if self.options.get("strict") is True:
                        raise err
                    else:
                        logger.warning(err.message)

                # enable UI customization
                self.set_ui_customization_enabled(
                    qgis3ini_filepath=cfg_qgis_base,
                    section="UI",
                    option="Customization\\enabled",
                    switch=True,
                )

                # set the splash screen into the customization file
                self.set_splash_screen(
                    qgiscustomization3ini_filepath=cfg_qgis_custom,
                    splash_screen_filepath=splash_screen_filepath.resolve(),
                    switch=True,
                )
        elif self.options.get("action") == "remove":
            for profile_dir in li_installed_profiles_path:
                # default absolute splash screen path
                splash_screen_filepath = profile_dir / self.DEFAULT_SPLASH_FILEPATH

                # target QGIS configuration files
                cfg_qgis_base = profile_dir / "QGIS/QGIS3.ini"
                cfg_qgis_custom = profile_dir / "QGIS/QGISCUSTOMIZATION3.ini"

                # set the splash screen into the customization file
                self.set_splash_screen(
                    qgiscustomization3ini_filepath=cfg_qgis_custom,
                    splash_screen_filepath=splash_screen_filepath.resolve(),
                    switch=False,
                )
        else:
            raise NotImplementedError

        logger.debug(f"Job {self.ID} ran successfully.")

    # -- INTERNAL LOGIC ------------------------------------------------------

    def set_splash_screen(
        self,
        qgiscustomization3ini_filepath: Path,
        splash_screen_filepath: Path = None,
        switch: bool = True,
    ) -> bool:
        """Add/remove splash screen path to the QGISCUSTOMIZATION3.ini file.

        Args:
            qgiscustomization3ini_filepath (Path): path to the QGISCUSTOMIZATION3.ini
                configuration file
            splash_screen_filepath (Path, optional): path to the folder containing the
                splash.png file, defaults to None. Defaults to None.
            switch (bool, optional): True to add, False to remove, defaults to True.
                Defaults to True.

        Returns:
            bool: True is the splash folder is present. False is absent.
        """
        # vars
        section = "Customization"
        option = "splashpath"
        if switch:
            # normalize splash screen folder path
            nrm_splash_screen_folder = normalize_path(
                splash_screen_filepath.parent, add_trailing_slash_if_dir=True
            )

        # make sure that the file exists
        if not qgiscustomization3ini_filepath.exists() and switch:
            logger.warning(
                f"Configuration file {qgiscustomization3ini_filepath} doesn't exist. "
                "It will be created but maybe it was not the expected behavior."
            )
            qgiscustomization3ini_filepath.touch(exist_ok=True)
            qgiscustomization3ini_filepath.write_text(
                data=f"[Customization]\nsplashpath={nrm_splash_screen_folder}",
                encoding="UTF8",
            )
            return switch
        elif not qgiscustomization3ini_filepath.exists() and not switch:
            logger.debug(
                f"'{qgiscustomization3ini_filepath} doesn't exist, so "
                "splash screen is DISABLED."
            )
            return switch

        # open
        ini_qgiscustom3 = ConfigParser()
        ini_qgiscustom3.optionxform = str
        ini_qgiscustom3.read(qgiscustomization3ini_filepath, encoding="UTF8")

        # check existing option value
        if ini_qgiscustom3.has_option(section=section, option=option):
            actual_state = ini_qgiscustom3.get(section=section, option=option)

            if not switch:
                ini_qgiscustom3.remove_option(section=section, option=option)
                with qgiscustomization3ini_filepath.open(
                    "w", encoding="UTF8"
                ) as configfile:
                    ini_qgiscustom3.write(configfile, space_around_delimiters=False)
                logger.debug(
                    f"Splash screen {splash_screen_filepath} has been "
                    f"DISABLED in {qgiscustomization3ini_filepath}"
                )
                return True
            elif actual_state == nrm_splash_screen_folder and switch:
                logger.debug(
                    f"Splash screen {splash_screen_filepath} is already "
                    f"ENABLED in {qgiscustomization3ini_filepath}"
                )
                return True
            elif actual_state != nrm_splash_screen_folder and switch:
                ini_qgiscustom3.set(
                    section=section,
                    option=option,
                    value=nrm_splash_screen_folder,
                )
                with qgiscustomization3ini_filepath.open(
                    "w", encoding="UTF8"
                ) as configfile:
                    ini_qgiscustom3.write(configfile, space_around_delimiters=False)
                logger.debug(
                    f"Splash screen {splash_screen_filepath} has been "
                    f"ENABLED in {qgiscustomization3ini_filepath}"
                )
                return True
            else:
                pass

        elif ini_qgiscustom3.has_section(section=section) and switch:
            # section exist but not the option, so let's add it as required
            ini_qgiscustom3.set(
                section=section,
                option=option,
                value=nrm_splash_screen_folder,
            )
            with qgiscustomization3ini_filepath.open(
                "w", encoding="UTF8"
            ) as configfile:
                ini_qgiscustom3.write(configfile, space_around_delimiters=False)
            logger.debug(
                f"'{option}' option was missing in {section}, it's just been added and "
                f"ENABLED in {qgiscustomization3ini_filepath}"
            )
            return True
        elif not ini_qgiscustom3.has_section(section=section) and switch:
            # even the section is missing. Let's add everything
            ini_qgiscustom3.add_section(section)
            ini_qgiscustom3.set(
                section=section,
                option=option,
                value=nrm_splash_screen_folder,
            )
            with qgiscustomization3ini_filepath.open(
                "w", encoding="UTF8"
            ) as configfile:
                ini_qgiscustom3.write(configfile, space_around_delimiters=False)
            logger.debug(
                f"'{option}' option was missing in {section}, it's just been added and "
                f"ENABLED in {qgiscustomization3ini_filepath}"
            )
            return True
        else:
            logger.debug(
                f"Section '{section}' is not present so "
                f"{option} is DISABLED in {qgiscustomization3ini_filepath}"
            )
            return False


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
