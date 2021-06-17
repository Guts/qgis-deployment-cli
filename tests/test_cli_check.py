#! python3  # noqa: E265

"""
    Tests against CLI check command.
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library

# 3rd party library
from click.testing import CliRunner

# module to test
from qgis_deployment_toolbelt.cli import qgis_deployment_toolbelt

# #############################################################################
# ######## Globals #################
# ##################################

# #############################################################################
# ######## Classes #################
# ##################################


def test_check_help():
    """Test help command"""
    runner = CliRunner()
    result = runner.invoke(
        qgis_deployment_toolbelt, ["--settings=./.env.example", "check", "--help"]
    )
    assert result.exit_code == 0


# #############################################################################
# ######## Standalone ##############
# ##################################
if __name__ == "__main__":
    pass
