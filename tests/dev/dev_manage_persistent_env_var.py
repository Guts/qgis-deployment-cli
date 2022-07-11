#! python3  # noqa: E265

# libraries
import winreg
from os.path import expandvars
from pathlib import Path
import win32gui


from py_setenv import setenv


def RefreshEnvironment():
    """A method by Geoffrey Faivre-Malloy and Ronny Lipshitz"""
    # broadcast settings change
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x001A
    SMTO_ABORTIFHUNG = 0x0002
    sParam = "Environment"

    res1, res2 = win32gui.SendMessageTimeout(
        HWND_BROADCAST, WM_SETTINGCHANGE, 0, sParam, SMTO_ABORTIFHUNG, 100
    )
    print(f"{bool(res1)}", res2)
    if not res1:
        print("result: %s, %s, from SendMessageTimeout" % (bool(res1), res2))


# variables
osgeo4w_dir_download: str = setenv(
    "OSGEO4W_DOWNLOAD_FOLDER", user=True, suppress_echo=True
)
osgeo4w_dir_install: str = setenv(
    "OSGEO4W_INSTALL_FOLDER_QGIS", user=True, suppress_echo=True
)
qgis_pyqgis_startup: str = setenv("PYQGIS_STARTUP", user=True, suppress_echo=True)
startup_script_path: Path = Path(
    r"C:\Users\risor\Documents\GitHub\Oslandia\ressources_formation\QGIS\QGIS9_administration\support\scripts\qgis_startup.py"
)
print(startup_script_path.is_file())

if not qgis_pyqgis_startup:
    print("PYQGIS_STARTUP is not set")
    setenv(
        "PYQGIS_STARTUP",
        value=str(startup_script_path.resolve()),
        user=True,
        suppress_echo=True,
    )
    qgis_pyqgis_startup: str = setenv("PYQGIS_STARTUP", user=True, suppress_echo=True)
    print(f"PYQGIS_STARTUP is now set: {len(qgis_pyqgis_startup)}")
else:
    print("PYQGIS_STARTUP already set: {}".format(len(qgis_pyqgis_startup)))

RefreshEnvironment()

# setenv(list_all=True, user=True)

# Manually

# registry = winreg.ConnectRegistry(key=winreg.HKEY_CURRENT_USER, r"Environment")
# import os

# os.system("setx PYQGIS_STARTUP {}".format(startup_script_path.resolve()))

