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
import distro
import PyInstaller.__main__

# package
sys.path.insert(0, str(Path(".").resolve()))
from qgis_deployment_toolbelt import __about__  # noqa: E402

# #############################################################################
# ########### MAIN #################
# ##################################
package_folder = Path("qgis_deployment_toolbelt")

PyInstaller.__main__.run(
    [
        "--add-data=LICENSE:.",
        "--add-data=README.md:.",
        "--add-data={}:profiles/".format(
            (package_folder / "profiles/shortcut_freedesktop.template/").resolve()
        ),
        "--log-level={}".format(getenv("PYINSTALLER_LOG_LEVEL", "WARN")),
        "--name={}_{}_{}{}_{}_Python{}".format(
            __about__.__title_clean__,
            __about__.__version__,
            distro.name(),
            distro.version(),
            platform.architecture()[0],
            platform.python_version(),
        ).replace(".", "-"),
        "--noconfirm",
        "--noupx",
        "--onefile",
        "--console",
        str(package_folder / "cli.py"),
    ]
)
