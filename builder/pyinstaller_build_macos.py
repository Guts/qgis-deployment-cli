#! python3  # noqa: E265

"""
    Launch PyInstaller using a Python script.
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import platform
import sys
from os import getenv
from pathlib import Path

# 3rd party
import PyInstaller.__main__

# package
sys.path.insert(0, str(Path(".").resolve()))
from qgis_deployment_toolbelt import __about__  # noqa: E402

# #############################################################################
# ########### MAIN #################
# ##################################
package_folder = Path("qgis_deployment_toolbelt")

mac_os_version, _, _ = platform.mac_ver()
mac_os_version = "-".join(mac_os_version.split(".")[:2])

PyInstaller.__main__.run(
    [
        "--log-level={}".format(getenv("PYINSTALLER_LOG_LEVEL", "WARN")),
        "--name={}_{}_MacOS{}_Python{}-{}".format(
            __about__.__title_clean__,
            __about__.__version__.replace(".", "-"),
            mac_os_version,
            platform.python_version_tuple()[0],
            platform.python_version_tuple()[1],
        ),
        "--noconfirm",
        "--noupx",
        "--onefile",
        "--console",
        str(package_folder / "cli.py"),
    ]
)
