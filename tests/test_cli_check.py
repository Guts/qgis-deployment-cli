#! python3  # noqa: E265

"""
    Test CLI's check command.
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import unittest
from pathlib import Path
from unittest import mock

# 3rd party library
from click.testing import CliRunner

# module to test
from qgis_deployment_toolbelt.cli import qgis_deployment_toolbelt
from qgis_deployment_toolbelt.commands import cli_check

# #############################################################################
# ######## Globals #################
# ##################################

sample_scenario_good: Path = Path(
    "tests/fixtures/scenarios/good_scenario_sample.qdt.yml"
)

# #############################################################################
# ######## Classes #################
# ##################################


def test_check_help():
    """Test help command"""
    runner = CliRunner()
    result = runner.invoke(
        qgis_deployment_toolbelt,
        [f"--scenario={str(sample_scenario_good.resolve())}", "check", "--help"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0


class TestCheck(unittest.TestCase):
    """Test module"""

    def test_cli_check(self):
        """Test check method from the cli_check module"""
        with self.assertRaises(SystemExit) as excinfo:
            cli_check.check()
        self.assertEqual(str(excinfo.exception), "0")


@mock.patch("qgis_deployment_toolbelt.commands.cli_check.opersys", "win32_fake")
class TestCheckImaginaryOpersys(unittest.TestCase):
    """Test module with a fake opersys variable"""

    def test_cli_check(self):
        """Test check method from the cli_check module"""
        with self.assertRaises(SystemExit) as excinfo:
            cli_check.check()
        self.assertEqual(str(excinfo.exception), "1")


# #############################################################################
# ######## Standalone ##############
# ##################################
if __name__ == "__main__":
    pass
