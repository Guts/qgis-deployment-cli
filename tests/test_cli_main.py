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
sample_scenario_good_with_unexisting_jobs: Path = Path(
    "tests/fixtures/scenarios/good_scenario_with_unexisting_jobs.qdt.yml"
)
sample_scenario_good_splash_removal: Path = Path(
    "tests/fixtures/scenarios/good_scenario_splash_screen_remove.qdt.yml"
)

sample_scenario_false: Path = Path(
    "tests/fixtures/scenarios/false_scenario_sample.qdt.yml"
)
sample_scenario_imaginary: Path = Path(
    "tests/fixtures/scenarios/imaginary_scenario_sample.qdt.yml"
)

good_scenarios = [
    ["deploy", f"--scenario={scenario_path.resolve()}"]
    for scenario_path in Path("tests/fixtures/scenarios/").glob("good_*.qdt.yml")
]

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


@pytest.mark.parametrize("option", good_scenarios)
def test_main_run(capsys, option):
    """Test main cli command"""
    with pytest.raises(SystemExit):
        cli.main(option)

    out, err = capsys.readouterr()
    assert err == ""


def test_main_run_unexising_jobs(capsys):
    """Test main cli command"""
    with pytest.raises(SystemExit):
        cli.main(
            [
                "deploy",
                f"--scenario={str(sample_scenario_good_with_unexisting_jobs.resolve())}",
            ]
        )

    out, err = capsys.readouterr()
    assert err == ""


def test_main_run_failed(capsys):
    """Test main cli command"""
    with pytest.raises(FileExistsError):
        cli.main(["deploy", f"--scenario={str(sample_scenario_false.resolve())}"])

    out, err = capsys.readouterr()
    assert err == ""


def test_main_run_removing_splash(capsys):
    """Test main cli command"""
    with pytest.raises(SystemExit):
        cli.main(
            ["deploy", f"--scenario={sample_scenario_good_splash_removal.resolve()}"]
        )

    out, err = capsys.readouterr()
    assert err == ""


# #############################################################################
# ######## Standalone ##############
# ##################################
if __name__ == "__main__":
    pass
