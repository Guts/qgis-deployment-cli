#! python3  # noqa: E265

"""
    Sub-command in charge of managing QGIS plugins.
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from datetime import datetime, timedelta
from pathlib import Path
from timeit import default_timer

# 3rd party library
import click

# submodules
from qgis_deployment_toolbelt.utils.bouncer import exit_cli_success

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
@click.group(
    context_settings=CONTEXT_SETTINGS,
    no_args_is_help=True,
)
def plugins(cli_context: click.Context):
    """List, install, uninstall, check QGIS plugins.

    \f
    :param click.core.Context cli_context: Click context
    :param bool remove_empty_folders: if passed, empty folders will be deleted too
    """

    # ending
    exit_cli_success(
        message="CLEAN completed after {:5.2f}s.".format(default_timer() - START_TIME),
        abort=False,
    )


# #############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """Standalone execution."""
    # launch cli
    plugins(obj={})
