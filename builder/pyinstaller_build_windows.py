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

PyInstaller.__main__.run(
    [
        "--add-data=LICENSE:.",
        "--add-data=README.md:.",
        "--add-data={}:profiles/".format(
            (package_folder / "profiles/shortcut_freedesktop.template/").resolve()
        ),
        # "--clean",
        f"--icon={package_folder.parent.resolve()}/docs/static/logo_qdt.ico",
        "--log-level={}".format(getenv("PYINSTALLER_LOG_LEVEL", "WARN")),
        "--manifest={}".format((package_folder / "../builder/manifest.xml").resolve()),
        "--name={}_{}_{}{}_Python{}-{}".format(
            __about__.__title_clean__,
            __about__.__version__.replace(".", "-"),
            platform.system(),
            platform.architecture()[0],
            platform.python_version_tuple()[0],
            platform.python_version_tuple()[1],
        ),
        "--noconfirm",
        "--noupx",
        # "--onefile",
        "--version-file={}".format("version_info.txt"),
        "--console",
        str(package_folder / "cli.py"),
    ]
)
