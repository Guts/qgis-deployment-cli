#! python3  # noqa: E265

"""
    Test CLI's check command.
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


# #############################################################################
# ######## Standalone ##############
# ##################################
if __name__ == "__main__":
    pass
