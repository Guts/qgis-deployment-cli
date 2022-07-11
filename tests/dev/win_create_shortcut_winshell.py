import os
import sys

import winshell

link_filepath = os.path.join(winshell.desktop(), "python.lnk")
with winshell.shortcut(link_filepath) as link:
    link.path = sys.executable
    link.description = "Shortcut to python"
    link.arguments = "-m winshell"
