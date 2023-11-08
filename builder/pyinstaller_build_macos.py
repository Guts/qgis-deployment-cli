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
from datetime import datetime
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
# write build report
build_report = (
    f"datetime: {datetime.now().astimezone().isoformat()}"
    f"\nprog_name: {__about__.__title__}"
    f"\nprog_version: {__about__.__version__}"
    f"\noperating_system: {platform.system()}"
    f"\noperating_system_version: {platform.release()}_{platform.version()}"
    f"\narchitecture: {platform.architecture()[0]}"
    f"\npython_version: {platform.python_version()}"
)
Path("build_environment_report.txt").write_text(data=build_report, encoding="UTF-8")

# variables
output_filename = f"{__about__.__title_clean__}_{__about__.__version__}"
package_folder = Path("qgis_deployment_toolbelt")


mac_os_version, _, _ = platform.mac_ver()
mac_os_version = "-".join(mac_os_version.split(".")[:2])

PyInstaller.__main__.run(
    [
        "--add-data=LICENSE:.",
        "--add-data=README.md:.",
        f"--add-data={package_folder.joinpath('profiles/shortcut_freedesktop.template/').resolve()}:profiles/",
        f"--log-level={getenv('PYINSTALLER_LOG_LEVEL', 'WARN')}",
        f"--name={output_filename}",
        "--noconfirm",
        # "--noupx",
        "--onefile",
        "--console",
        str(package_folder / "cli.py"),
    ]
)
