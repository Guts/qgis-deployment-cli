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
import subprocess
from os.path import expandvars
from pathlib import Path
from shutil import which
from sys import platform as opersys

# package
from qgis_deployment_toolbelt.exceptions import QgisInstallNotFound
from qgis_deployment_toolbelt.jobs.generic_job import GenericJob

# #############################################################################
# ########## Globals ###############
# ##################################


# logs
logger = logging.getLogger(__name__)

# #############################################################################
# ########## Classes ###############
# ##################################


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
            "default": "warning",
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
        if not self.run_needed():
            return

        if opersys not in ("linux", "win32"):
            logger.error(f"This job does not support your operating system: {opersys}")
            return

        installed_qgis_path: str | None = self.get_installed_qgis_path()

        if installed_qgis_path:
            os.environ["QDT_QGIS_EXE_PATH"] = installed_qgis_path
        else:
            if self.options.get("if_not_found", "warning") == "error":
                raise QgisInstallNotFound()
            else:
                logger.warning("No QGIS installation found")

        # log
        logger.debug(f"Job {self.ID} ran successfully.")

    # -- INTERNAL LOGIC ------------------------------------------------------
    def run_needed(self) -> bool:
        """Check if job run is needed

        Returns:
            bool: return True if job must be run, False otherwise
        """
        if "QDT_QGIS_EXE_PATH" in os.environ:
            qgis_bin = os.environ["QDT_QGIS_EXE_PATH"]
            if Path(qgis_bin).exists():
                version_str = self._get_qgis_bin_version(qgis_bin)
                if version_str:
                    logger.info(
                        f"QDT_QGIS_EXE_PATH defined and path {qgis_bin} exists for QGIS {version_str}. {self.ID} job is skipped. "
                    )
                    return False
                else:
                    logger.warning(
                        f"QDT_QGIS_EXE_PATH defined and path {qgis_bin} exists but the QGIS version can't be defined. Check variable."
                    )
        return True

    def get_installed_qgis_path(self) -> str | None:
        """Get list of installed qgis

        Returns:
            str | None : installed qgis path
        """
        if opersys == "linux":
            found_versions = self._get_linux_installed_qgis_path()
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

        version_priority: list[str] = []
        if "version_priority" in self.options:
            version_priority = self.options["version_priority"]

        # Add preferred qgis version on top of the list
        if "QDT_PREFERRED_QGIS_VERSION" in os.environ:
            version_priority.insert(0, os.environ["QDT_PREFERRED_QGIS_VERSION"])

        for version in version_priority:
            if latest_matching_version := self._get_latest_matching_version_path(
                found_versions=found_versions, version=version
            ):
                return latest_matching_version

            version_priority_str = ",".join(self.options["version_priority"])
            logger.info(
                f"QGIS version(s) [{version_priority_str}] not found. Using most recent found version {latest_version} : {latest_qgis}"
            )

        return latest_qgis

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
                install_dir = os.path.join(prog_file_dir, dir_name)
                if qgis_bin := JobQgisInstallationFinder._get_qgis_bin_in_install_dir(
                    install_dir
                ):
                    version_str = JobQgisInstallationFinder._get_qgis_bin_version(
                        qgis_bin=qgis_bin
                    )
                    if version_str:
                        found_version[version_str] = qgis_bin
                    else:
                        logger.warning(
                            f"Can't define QGIS version for '{qgis_bin}' binary."
                        )

        # OSGEO4W
        install_dir = os.environ.get("QDT_OSGEO4W_INSTALL_DIR", "C:\\OSGeo4W")
        if qgis_bin := JobQgisInstallationFinder._get_qgis_bin_in_install_dir(
            install_dir
        ):
            version_str = JobQgisInstallationFinder._get_qgis_bin_version(
                qgis_bin=qgis_bin
            )
            if version_str:
                found_version[version_str] = qgis_bin
            else:
                logger.warning(f"Can't define QGIS version for '{qgis_bin}' binary.")

        return found_version

    @staticmethod
    def _get_linux_installed_qgis_path() -> dict[str, str]:
        """Get install qgis path for linux operating system with which

        Returns:
            dict[str, str]: dict of QGIS version and QGIS bin path
        """
        # use which to find installed qgis
        found_version = {}
        if qgis_bin := which("qgis"):
            logger.debug(f"QGIS path found using which: {qgis_bin}")
            version_str = JobQgisInstallationFinder._get_qgis_bin_version(
                qgis_bin=qgis_bin
            )
            if version_str:
                found_version[version_str] = qgis_bin
            else:
                logger.warning(f"Can't define QGIS version for '{qgis_bin}' binary.")

        return found_version

    @staticmethod
    def _get_qgis_bin_version(qgis_bin: str) -> str | None:
        """Get QGIS bin version with --version

        Args:
            qgis_bin (str): QGIS bin path

        Returns:
            str | None: SemVer version, None if version not found
        """
        process = subprocess.Popen(
            f'"{qgis_bin}" --version', stdout=subprocess.PIPE, shell=True
        )
        stdout_, _ = process.communicate()
        version_str = stdout_.decode()
        version_pattern = r"QGIS (\d+\.\d+\.\d+)-(\w+).*"
        version_match = re.match(version_pattern, version_str)
        if version_match:
            return version_match.group(1)
        return None
