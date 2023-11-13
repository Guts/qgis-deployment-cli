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
from pathlib import Path

# package
from qgis_deployment_toolbelt.exceptions import SplashScreenBadDimensions
from qgis_deployment_toolbelt.jobs.generic_job import GenericJob
from qgis_deployment_toolbelt.profiles.qdt_profile import QdtProfile
from qgis_deployment_toolbelt.profiles.qgis_ini_handler import QgisIniHelper
from qgis_deployment_toolbelt.utils.check_image_size import check_image_dimensions

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
        super().__init__()
        self.options: dict = self.validate_options(options)

    def run(self) -> None:
        """Execute job logic."""
        # check of there are some profiles folders within the downloaded folder
        downloaded_profiles = self.list_downloaded_profiles()
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
                qini_helper = QgisIniHelper(
                    ini_filepath=profile_downloaded.path_in_qgis / "QGIS/QGIS3.ini"
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
                qini_helper.set_ui_customization_enabled(
                    switch=True,
                )

                # set the splash screen into the customization file
                qini_helper.set_splash_screen(
                    ini_file=qini_helper.profile_customization_path,
                    splash_screen_filepath=splash_screen_filepath.resolve(),
                    switch=True,
                )
        elif self.options.get("action") == "remove":
            for profile_dir in li_installed_profiles_path:
                # default absolute splash screen path
                splash_screen_filepath = profile_dir / self.DEFAULT_SPLASH_FILEPATH

                # target QGIS configuration files
                cfg_qgis_custom = profile_dir / "QGIS/QGISCUSTOMIZATION3.ini"

                # set the splash screen into the customization file
                qini_helper.set_splash_screen(
                    ini_file=cfg_qgis_custom,
                    splash_screen_filepath=splash_screen_filepath.resolve(),
                    switch=False,
                )
        else:
            raise NotImplementedError

        logger.debug(f"Job {self.ID} ran successfully.")


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
