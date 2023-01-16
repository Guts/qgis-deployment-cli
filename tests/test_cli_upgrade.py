#! python3  # noqa: E265

"""
    Test CLI's clean command.

    Author: Julien Moura (Oslandia)
"""

# #############################################################################
# ########## Libraries #############
# ##################################

import shutil

# Standard library
import unittest
from pathlib import Path

# 3rd party library
from click.testing import CliRunner

# module to test
from qgis_deployment_toolbelt.cli import qgis_deployment_toolbelt

# #############################################################################
# ######## Classes #################
# ##################################


def test_upgrade_check():
    """Test help command"""
    runner = CliRunner()
    result = runner.invoke(
        qgis_deployment_toolbelt,
        ["upgrade", "-c"],
    )


def test_upgrade_download():
    """Test help command"""
    runner = CliRunner()
    result = runner.invoke(
        qgis_deployment_toolbelt,
        ["upgrade"],
    )


# #############################################################################
# ######## Standalone ##############
# ##################################
if __name__ == "__main__":
    pass
