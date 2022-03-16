#! python3  # noqa: E265

"""
    Main command-line.
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from pathlib import Path
from timeit import default_timer

# 3rd party library
import click

# submodules
# from qgis_deployment_toolbelt import LogManager
from qgis_deployment_toolbelt.__about__ import __version__
from qgis_deployment_toolbelt.commands import cli_check, cli_clean, cli_environment
from qgis_deployment_toolbelt.scenarios import ScenarioReader
from qgis_deployment_toolbelt.utils.bouncer import exit_cli_error

# #############################################################################
# ########## Globals ###############
# ##################################

# chronometer
START_TIME = default_timer()

# logs
logger = logging.getLogger(__name__)
log_console_handler = logging.StreamHandler()
logger.addHandler(log_console_handler)

# default CLI context.
# See: https://click.palletsprojects.com/en/7.x/commands/#context-defaults
CONTEXT_SETTINGS = dict(obj={})

# #############################################################################
# ####### Command-line ############
# #################################


@click.group(
    chain=True,
    invoke_without_command=True,
    context_settings=CONTEXT_SETTINGS,
)
@click.option(
    "-c",
    "--clear",
    is_flag=True,
    show_default=True,
    help="Clear the terminal before the execution.",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    show_default=True,
    help="Set output verbosity to the maximum level, overriding the configuration option.",
)
@click.option(
    "-s",
    "--scenario",
    default="scenario.qdt.yml",
    show_default=True,
    help="Scenario file to use.",
    type=click.Path(readable=True, file_okay=True, dir_okay=False, resolve_path=True),
)
@click.version_option(
    version=__version__,
    message="%(version)s",
    help="Display CLI version",
)
@click.pass_context
def qgis_deployment_toolbelt(
    cli_context: click.Context,
    scenario: Path,
    clear: bool,
    verbose: bool,
):
    """Main command.

    \f
    Args:
        cli_context (click.Context): Click context
        scenario (Path): path to a scenario file to use
        clear (bool): option to clear the terminal berfore any other step
        verbose (bool): option to force the verbose mode

    :Example:

        .. code-block:: powershell

            qgis-deployment-toolbelt -c --verbose check

    """
    # let's be clear or not
    if clear:
        click.clear()

    # -- LOG/VERBOSITY MANAGEMENT ------------------------------------------------------
    # if verbose, override conf value
    if verbose:
        logger.setLevel(logging.DEBUG)
        for h in logger.handlers:
            h.setLevel(logging.DEBUG)
    logger.info(f"{logging.getLevelName(logger.getEffectiveLevel())} mode enabled.")

    click.echo(
        "Timestamp: {} started after {:5.2f}s.".format(
            cli_context.info_name, default_timer() - START_TIME
        )
    )

    # -- USING DEFAULT SCENARIO OR NOT -------------------------------------------------
    # si pas de fichier scenario par défaut
    # et si pas de sous-commande

    if cli_context.invoked_subcommand is None:
        logger.debug(
            "Command-line invoked subcommand: {}.".format(
                cli_context.invoked_subcommand
            )
        )

    else:
        logger.debug(f"I am about to invoke {cli_context.invoked_subcommand}")

    # -- LOAD CONFIGURATION FILE -------------------------------------------------------
    if cli_context.invoked_subcommand:
        logger.error(
            "Command-line invoked subcommand: {}.".format(
                cli_context.invoked_subcommand
            )
        )

    if not scenario or not Path(scenario).exists():
        logger.error("Scenario file is not a file: {}".format(scenario))

    # end
    logger.debug(
        "Timestamp: {} completed after {:5.2f}s.".format(
            cli_context.info_name, default_timer() - START_TIME
        )
    )


# -- SUB-COMMANDS ----------------------------------------------------------------------
# Add subcommands to the main command group
qgis_deployment_toolbelt.add_command(cli_environment.environment_setup)
qgis_deployment_toolbelt.add_command(cli_check.check)
qgis_deployment_toolbelt.add_command(cli_clean.clean)

# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    # launch cli
    qgis_deployment_toolbelt(obj={})
    # logging.basicConfig(level=logging.DEBUG, )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
