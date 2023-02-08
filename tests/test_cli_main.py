#! python3  # noqa: E265

"""
    Test CLI's main command.

    Author: Julien Moura (Oslandia)
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from pathlib import Path

# 3rd party library
from click.testing import CliRunner

# module to test
from qgis_deployment_toolbelt.cli import qgis_deployment_toolbelt

# #############################################################################
# ######## Globals #################
# ##################################

sample_scenario_good: Path = Path(
    "tests/fixtures/scenarios/good_scenario_sample.qdt.yml"
)
sample_scenario_false: Path = Path(
    "tests/fixtures/scenarios/false_scenario_sample.qdt.yml"
)
sample_scenario_imaginary: Path = Path(
    "tests/fixtures/scenarios/imaginary_scenario_sample.qdt.yml"
)

# #############################################################################
# ######## Classes #################
# ##################################


def test_main_help():
    """Test help command"""
    runner = CliRunner()
    result = runner.invoke(
        qgis_deployment_toolbelt,
        ["--help"],
    )
    assert result.exit_code == 0


def test_main_run():
    """Test main cli command"""
    runner = CliRunner()
    result = runner.invoke(
        qgis_deployment_toolbelt,
        [f"--scenario={str(sample_scenario_good.resolve())}"],
    )
    assert result.exit_code == 0

    result = runner.invoke(
        qgis_deployment_toolbelt,
        [f"--scenario={str(sample_scenario_imaginary.resolve())}"],
    )
    assert result.exit_code == 1


def test_main_run_with_disable_validation_option():
    """Test main cli command with the disable validation option"""
    runner = CliRunner()
    result = runner.invoke(
        qgis_deployment_toolbelt,
        [f"--scenario={str(sample_scenario_good.resolve())}", "--disable-validation"],
    )
    assert result.exit_code == 0

    result = runner.invoke(
        qgis_deployment_toolbelt,
        [f"--scenario={str(sample_scenario_false.resolve())}", "--disable-validation"],
    )
    assert result.exit_code == 1


# #############################################################################
# ######## Standalone ##############
# ##################################
if __name__ == "__main__":
    pass
