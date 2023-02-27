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
import pytest

# module to test
from qgis_deployment_toolbelt import cli

# #############################################################################
# ######## Classes #################
# ##################################


def test_cli_upgrade_check_only(capsys):
    """Test CLI upgrade check only."""
    with pytest.raises(SystemExit):
        cli.main(["upgrade", "-c"])

    out, err = capsys.readouterr()

    assert err == ""


def test_cli_upgrade_download(capsys):
    """Test CLI upgrade ."""
    with pytest.raises(SystemExit):
        cli.main(["upgrade", "-n", "-w", "tests/"])

    out, err = capsys.readouterr()

    assert err == ""


# #############################################################################
# ######## Standalone ##############
# ##################################
if __name__ == "__main__":
    pass
