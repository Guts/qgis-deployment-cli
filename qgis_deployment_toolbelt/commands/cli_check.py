#! python3  # noqa: E265


"""
    Sub-command in charge of checking settings and environment.

"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from platform import platform
from pprint import pprint
from timeit import default_timer

# 3rd party library
import click

# submodules
from qgis_deployment_toolbelt.utils.bouncer import exit_cli_error, exit_cli_success

# #############################################################################
# ########## Globals ###############
# ##################################

# chronometer
START_TIME = default_timer()

# logs
logger = logging.getLogger(__name__)

# default CLI context.
# See: https://click.palletsprojects.com/en/7.x/commands/#context-defaults
CONTEXT_SETTINGS = dict(obj={})


# #############################################################################
# ####### Command-line ############
# #################################
@click.command(name="check")
@click.pass_context
def check(cli_context: click.Context):
    """Perform checks about CLI requirements.

    Args:
        cli_context (click.Context): Click context
    """
    logger.info("CHECK started after {:5.2f}s.".format(default_timer() - START_TIME))

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
    check(obj={})
