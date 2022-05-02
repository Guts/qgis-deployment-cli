#! python3  # noqa: E265


"""
    Check and set up the QGIS environment.
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import json
import logging
from pathlib import Path
from timeit import default_timer

# 3rd party library
import click

from qgis_deployment_toolbelt.jobs.job_environment_variables import (
    JobEnvironmentVariables,
)

# submodules
from qgis_deployment_toolbelt.utils.bouncer import exit_cli_error, exit_cli_success

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)

# default CLI context.
# See: https://click.palletsprojects.com/en/7.x/commands/#context-defaults
CONTEXT_SETTINGS = dict(obj={})


# #############################################################################
# ####### Command-line ############
# #################################
@click.command(name="env-setup")
@click.option(
    "-d",
    "--deployment-configuration",
    help="Deployment scenario configuration (.json).",
    default="deployment-config.json",
    show_default=True,
    type=click.Path(
        exists=True, readable=True, file_okay=True, dir_okay=False, resolve_path=True
    ),
)
@click.pass_context
def environment_setup(cli_context: click.Context, deployment_configuration: Path):
    """Set up the system environment for QGIS.

    Args:
        cli_context (click.Context): Click context
    """
    # chronometer
    START_TIME = default_timer()
    logger.info("CHECK started after {:5.2f}s.".format(default_timer() - START_TIME))

    with Path(deployment_configuration).open("r") as f:
        scenario_data = json.load(f)

    env_manager = JobEnvironmentVariables()
    env_manager.run(scenario_data.get("environment_variables"))

    # ending
    exit_cli_success(
        message="CHECK completed after {:5.2f}s.".format(default_timer() - START_TIME),
        abort=False,
    )


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    # launch cli
    environment_setup(obj={})
