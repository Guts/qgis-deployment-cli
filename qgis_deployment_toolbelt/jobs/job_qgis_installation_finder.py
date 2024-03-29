#! python3  # noqa: E265

"""
    Tools to find installed QGIS version

    Author: Jean-Marie KERLOCH (https://github.com/jmkerloch)
"""

# #############################################################################
# ########## Libraries #############
# ##################################


# Standard library
import logging
import os
import re
from os.path import expandvars
from shutil import which
from sys import platform as opersys

# package
from qgis_deployment_toolbelt.jobs.generic_job import GenericJob

# #############################################################################
# ########## Globals ###############
# ##################################


# logs
logger = logging.getLogger(__name__)

# #############################################################################
# ########## Classes ###############
# ##################################

OSGEO4W_VERSION = "OSGeo4W"
OSGEO4W_64_VERSION = "OSGeo4W64"


class JobQgisInstallationFinder(GenericJob):
    """
    Class to find installed QGIS version
    """

    ID: str = "qgis-installation-finder"
    OPTIONS_SCHEMA: dict = {
        "version_priority": {
            "type": (list, str),
            "required": False,
            "default": None,
            "possible_values": None,
            "condition": None,
        },
        "if_not_found": {
            "type": str,
            "required": False,
            "default": "error",
            "possible_values": ("warning", "error"),
            "condition": "in",
        },
    }

    def __init__(self, options: dict) -> None:
        """Instantiate the class.
        Args:
            options (dict): job options
        """

        super().__init__()
        self.options: dict = self.validate_options(options)

    def run(self) -> None:
        """Define QDT_QGIS_EXE_PATH for shortcut creation"""

        if opersys not in ("linux", "win32"):
            logger.error(f"This job does not support your operating system: {opersys}")
            return

        installed_qgis_path: str | None = self.get_installed_qgis_path()

        if installed_qgis_path:
            os.environ["QDT_QGIS_EXE_PATH"] = installed_qgis_path

        # log
        logger.debug(f"Job {self.ID} ran successfully.")

    # -- INTERNAL LOGIC ------------------------------------------------------
    def get_installed_qgis_path(self) -> str | None:
        """Get list of installed qgis

        Returns:
            str | None : installed qgis path
        """
        if opersys == "linux":
            return self._get_linux_installed_qgis_path()
        elif opersys == "win32":
            # Check for installed version in the default install directory
            found_versions = self._get_windows_installed_qgis_path()
            if len(found_versions) == 0:
                return None

            logger.debug(f"Found installed QGIS : {found_versions}")
            latest_version = self._get_latest_version_from_list(
                versions=list(found_versions.keys())
            )
            latest_qgis = found_versions[latest_version]

            if "version_priority" in self.options:
                for version in self.options["version_priority"]:
                    if latest_matching_version := self._get_latest_matching_version_path(
                        found_versions=found_versions, version=version
                    ):
                        return latest_matching_version
                version_priority_str = ",".join(self.options["version_priority"])
                logger.info(
                    f"QGIS version(s) [{version_priority_str}] not found. Using latest found version {latest_qgis}"
                )

            return latest_qgis
        return None

    @staticmethod
    def _get_latest_version_from_list(versions: list[str]) -> str | None:
        """Get latest version from a list, OSGEO4W are last

        Args:
            versions (list[str]): list of found version

        Returns:
            str | None: latest version, None if no version provided
        """
        if len(versions):
            used_version = versions
            used_version.sort(reverse=True)
            # OSGEO4W version must be check last because we can't define version
            if OSGEO4W_VERSION in used_version:
                used_version.remove(OSGEO4W_VERSION)
                used_version.append(OSGEO4W_VERSION)
            if OSGEO4W_64_VERSION in used_version:
                used_version.remove(OSGEO4W_64_VERSION)
                used_version.append(OSGEO4W_64_VERSION)
            return used_version[0]
        return None

    @staticmethod
    def _get_latest_matching_version_path(
        found_versions: dict[str, str], version: str
    ) -> str | None:
        """Get latest version path matching a wanted version

        Args:
            found_versions (dict[str, str]): dict of found versions
            version (str): wanted version

        Returns:
            str | None: latest matching version path, None if not found
        """
        match_versions = []
        for found_version in found_versions.keys():
            if found_version.startswith(version):
                match_versions.append(found_version)
        # Use latest version
        if latest_version := JobQgisInstallationFinder._get_latest_version_from_list(
            match_versions
        ):
            return found_versions[latest_version]
        return None

    @staticmethod
    def _get_qgis_bin_in_install_dir(install_dir: str) -> str | None:
        """Get QGIS binary path from an install directory

        Args:
            install_dir (str): install directory

        Returns:
            str | None: QGIS bin path, None if not found
        """
        binary_pattern = re.compile(r"qgis(-ltr)?-bin\.exe", re.IGNORECASE)
        # Check if the bin directory exists within this directory
        bin_dir = os.path.join(install_dir, "bin")
        if os.path.exists(bin_dir):
            # Check if any binary file matches the pattern in the bin directory
            for filename in os.listdir(bin_dir):
                if binary_pattern.match(filename):
                    qgis_exe = os.path.join(bin_dir, filename)
                    return qgis_exe
        return None

    @staticmethod
    def _get_windows_installed_qgis_path() -> dict[str, str]:
        """Get dict of installed QGIS version in common install directory

        Returns:
            dict[str, str]: dict of QGIS version and QGIS bin path
        """
        # Check for installed version in the default install directory
        found_version = {}

        # Program files
        prog_file_dir = expandvars("%PROGRAMFILES%")
        directory_pattern = re.compile(r"QGIS (\d+)\.(\d+)\.(\d+)", re.IGNORECASE)
        for dir_name in os.listdir(prog_file_dir):
            # Check if the directory name matches the pattern
            match = directory_pattern.match(dir_name)
            if match:
                version = match.group(1) + "." + match.group(2) + "." + match.group(3)
                install_dir = os.path.join(prog_file_dir, dir_name)
                if qgis_exe := JobQgisInstallationFinder._get_qgis_bin_in_install_dir(
                    install_dir
                ):
                    found_version[version] = qgis_exe

        # OSGEO4W
        install_dir = "C:\\OSGeo4W"
        if qgis_exe := JobQgisInstallationFinder._get_qgis_bin_in_install_dir(
            install_dir
        ):
            found_version[OSGEO4W_VERSION] = qgis_exe

        # OSGEO4W64
        install_dir = "C:\\OSGeo4W64"
        if qgis_exe := JobQgisInstallationFinder._get_qgis_bin_in_install_dir(
            install_dir
        ):
            found_version[OSGEO4W_64_VERSION] = qgis_exe

        return found_version

    @staticmethod
    def _get_linux_installed_qgis_path() -> str | None:
        """Get install qgis path for linux operating system with which

        Returns:
            str | None: qgis install path, None if not found
        """
        # use which to find installed qgis
        if which_qgis_path := which("qgis"):
            logger.debug(f"QGIS path found using which: {which_qgis_path}")
            return which_qgis_path
        return None
