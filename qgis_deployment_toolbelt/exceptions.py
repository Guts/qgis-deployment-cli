#! python3  # noqa: E265

"""Custom exceptions."""

# standard library
from pathlib import Path

# package
from qgis_deployment_toolbelt.utils.check_image_size import get_image_size


class SplashScreenBadDimensions(Exception):
    """When splash screen image does not comply with recomended dimensions."""

    def __init__(self, image_filepath: Path, profile_name: str = None):
        """Initialization method.

        :param Path image_filepath: path to the selected image to be set as splash screen
        """
        self.message = (
            f"Profile {profile_name} -"
            f"{image_filepath.resolve()} dimensions "
            f"{get_image_size(image_filepath=image_filepath)} do not comply with "
            " dimensions recomended by QGIS for splash screen: 600x300."
        )
        super().__init__(self.message)
