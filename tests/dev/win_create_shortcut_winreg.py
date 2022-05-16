#! python3  # noqa: E265

import os
import sys
import sysconfig
import winreg

from win32com.client import Dispatch


def get_reg(name, path):
    # Read variable from Windows Registry
    # From http://stackoverflow.com/a/35286642
    try:
        registry_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_READ
        )
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None


# Package name
packageName = "iromlab"

# Scripts directory (location of launcher script)
scriptsDir = sysconfig.get_path("scripts")

# Target of shortcut
target = sys.executable

# Name of link file
linkName = packageName + ".lnk"

# Read location of Windows desktop folder from registry
regName = "Desktop"
regPath = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
desktopFolder = os.path.normpath(get_reg(regName, regPath))

# Path to location of link file
pathLink = os.path.join(desktopFolder, linkName)
shell = Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(pathLink)
shortcut.Targetpath = target
shortcut.WorkingDirectory = scriptsDir
shortcut.IconLocation = target
shortcut.save()
