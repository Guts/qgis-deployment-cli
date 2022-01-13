#! python3  # noqa: E265

"""
    Command-line to sycnhronize Scan results.

    Author: Isogeo
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


def test_clean_help():
    """Test help command"""
    runner = CliRunner()
    result = runner.invoke(
        qgis_deployment_toolbelt, ["--settings=.env.example", "clean", "--help"]
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


# #############################################################################
# ######## Standalone ##############
# ##################################
if __name__ == "__main__":
    pass
