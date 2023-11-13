import configparser
from os import PathLike
from pathlib import Path
from typing import Any


class CustomConfigParser(configparser.ConfigParser):
    """CustomConfigParser extends configparser.ConfigParser to include
    functionality for storing the paths of the INI files being read.

    Attributes:
        initial_file_path (str | PathLike | None): path of the initial ini file from
            which the configurations were loaded.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the CustomConfigParser with the same arguments as
        configparser.ConfigParser.
        """
        super().__init__(*args, **kwargs)
        self.initial_file_path: str | PathLike | None = None

    def read(self, ini_filepath: str | PathLike, *args: Any, **kwargs: Any) -> None:
        """Read and parse filenames, storing the file paths.

        Args:
            ini_filepath ( str | PathLike): The paths of
                the INI files to be read.
        """
        super().read(ini_filepath, *args, **kwargs)
        self.initial_file_path = ini_filepath

    def get_initial_file_path(self) -> Path | None:
        """Get the stored file path of the initial INI file as pathlib.Path object.

        Returns:
            Path: path to the initial INI file that have been read.
        """
        if self.initial_file_path is not None:
            return Path(self.initial_file_path)
        return None


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    # Exemple d'utilisation
    # Exemple d'utilisation
    config = CustomConfigParser()
    config.read(["votre_fichier1.ini", "votre_fichier2.ini"])

    print("Chemins des fichiers INI:", config.get_file_paths())
