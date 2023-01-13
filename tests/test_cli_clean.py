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
from qgis_deployment_toolbelt.commands import cli_clean

# #############################################################################
# ######## Globals #################
# ##################################

sample_scenario_good: Path = Path(
    "tests/fixtures/scenarios/good_scenario_sample.qdt.yml"
)

# #############################################################################
# ######## Classes #################
# ##################################


def test_clean_help():
    """Test help command"""
    runner = CliRunner()
    result = runner.invoke(
        qgis_deployment_toolbelt,
        [f"--scenario={str(sample_scenario_good.resolve())}", "clean", "--help"],
    )
    assert result.exit_code == 0


# def test_clean_minimal_params():
#     """Test minimal required parameters"""
#     runner = CliRunner()
#     result = runner.invoke(qgis_deployment_toolbelt, ["--settings=./.env.example",])
#     assert result.exit_code == 0


# def test_clean_complete_params():
#     """Test maximal parameters"""
#     runner = CliRunner()
#     result = runner.invoke(
#         qgis_deployment_toolbelt,
#         [
#             "--label=UnitTests",
#             "--settings=./.env.example",
#             "--formats=shp",
#             "--directory=./tests/fixtures",
#         ],
#     )
#     assert result.exit_code == 0


class TestClean(unittest.TestCase):
    """Test module"""

    def test_cli_clean(self):
        """Test clean method from the cli_clean module"""
        logs_dir = Path().resolve() / "_logs"
        logs_subdir = logs_dir / "log1"
        shutil.rmtree(logs_dir, ignore_errors=True)
        with self.assertRaises(SystemExit) as excinfo:
            cli_clean.clean()
        self.assertEqual(str(excinfo.exception), "1")

        logs_dir.mkdir(parents=True, exist_ok=True)
        logs_subdir.mkdir(parents=True, exist_ok=True)
        with self.assertRaises(SystemExit) as excinfo:
            cli_clean.clean()
        self.assertEqual(str(excinfo.exception), "0")


# #############################################################################
# ######## Standalone ##############
# ##################################
if __name__ == "__main__":
    pass
