#! python3  # noqa: E265
from distutils import spawn
from pathlib import Path

# See: pip install windows-tools.installed-software
from windows_tools.installed_software import get_installed_software

# standard library
print(spawn.find_executable("qgis-ltr-bin.exe", path="C:\\Program Files\\"))

result = get_installed_software()
for i in result:
    if "qgis" in i.get("name").lower():
        print(i)
