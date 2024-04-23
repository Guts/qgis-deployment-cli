#! python3  # noqa: E265

"""
    Test CLI's rules context export command.

    Author: Julien Moura (Oslandia)
"""

# #############################################################################
# ########## Libraries #############
# ##################################


# 3rd party
import pytest

# project
from qgis_deployment_toolbelt import cli

# #############################################################################
# ######## Classes #################
# ##################################


@pytest.mark.parametrize("option", ("-h", "--help"))
def test_cli_export_rules_context_help(capsys, option):
    """Test CLI help."""
    with pytest.raises(SystemExit):
        cli.main(["export-rules-context", option])

    out, err = capsys.readouterr()

    assert err == ""


def test_cli_export_rules_context(capsys):
    """Test CLI."""
    with pytest.raises(SystemExit):
        cli.main(["export-rules-context"])

    out, err = capsys.readouterr()

    assert err == ""


# #############################################################################
# ######## Standalone ##############
# ##################################
if __name__ == "__main__":
    pass
