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

# 3rd party
import pytest

# module to test
from qgis_deployment_toolbelt import __about__, cli

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


@pytest.mark.parametrize("option", ("-h", "--help"))
def test_cli_help(capsys, option):
    """Test CLI help."""
    with pytest.raises(SystemExit):
        cli.main([option])

    out, err = capsys.readouterr()

    assert (
        f"{__about__.__title__} {__about__.__version__} - {__about__.__summary__}"
        in out
    )
    assert err == ""


@pytest.mark.parametrize("option", (["--version"]))
def test_cli_version(capsys, option):
    """Test CLI version."""
    with pytest.raises(SystemExit):
        cli.main([option])

    out, err = capsys.readouterr()

    assert f"{__about__.__version__}\n" == out

    assert err == ""


def test_main_run(capsys):
    """Test main cli command"""
    # runner = CliRunner()
    # result = runner.invoke(
    #     qgis_deployment_toolbelt,
    #     [],
    # )
    # assert result.exit_code == 0

    # result = runner.invoke(
    #     qgis_deployment_toolbelt,
    #     [f"--scenario={str(sample_scenario_imaginary.resolve())}"],
    # )
    # assert result.exit_code == 1

    with pytest.raises(SystemExit):
        cli.main(["deploy", f"--scenario={str(sample_scenario_good.resolve())}"])

    out, err = capsys.readouterr()
    assert err == ""


# def test_main_run_with_disable_validation_option():
#     """Test main cli command with the disable validation option"""
#     runner = CliRunner()
#     result = runner.invoke(
#         qgis_deployment_toolbelt,
#         [f"--scenario={str(sample_scenario_good.resolve())}", "--disable-validation"],
#     )
#     assert result.exit_code == 0

#     result = runner.invoke(
#         qgis_deployment_toolbelt,
#         [f"--scenario={str(sample_scenario_false.resolve())}", "--disable-validation"],
#     )
#     assert result.exit_code == 1


# #############################################################################
# ######## Standalone ##############
# ##################################
if __name__ == "__main__":
    pass
