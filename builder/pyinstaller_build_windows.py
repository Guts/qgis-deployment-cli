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
Path(
    f"build_environment_report_Windows_{platform.release()}_{platform.version()}.txt"
).write_text(data=build_report, encoding="UTF-8")

# variables
output_filename = (
    f"Windows_{__about__.__title_clean__}_{__about__.__version__.replace('.', '-')}"
)
package_folder = Path("qgis_deployment_toolbelt")

PyInstaller.__main__.run(
    [
        "--add-data=LICENSE:.",
        "--add-data=README.md:.",
        # "--clean",
        f"--icon={package_folder.parent.resolve()}/docs/static/logo_qdt.ico",
        f"--log-level={getenv('PYINSTALLER_LOG_LEVEL', 'WARN')}",
        f"--manifest={Path(__file__).parent.joinpath('manifest.xml')}",
        f"--name={output_filename}",
        "--noconfirm",
        # "--noupx",
        "--onefile",
        "--version-file=version_info.txt",
        "--console",
        str(package_folder / "cli.py"),
    ]
)
