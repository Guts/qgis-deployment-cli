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
from qgis_deployment_toolbelt import LogManager
from qgis_deployment_toolbelt.__about__ import __version__
from qgis_deployment_toolbelt.commands import cli_check, cli_clean
from qgis_deployment_toolbelt.utils.bouncer import exit_cli_error

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
    chain=True,
    invoke_without_command=True,
    context_settings=CONTEXT_SETTINGS,
    no_args_is_help=True,
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
    "-l",
    "--label",
    help="Personnaliser le nom de la tâche, utilisé notamment pour nommer le fichier "
    "journal (log).",
    default="tactis_qgis_deployment_toolbelt",
    show_default=True,
)
@click.option(
    "-s",
    "--settings",
    default="default.conf",
    show_default=True,
    prompt="Configuration file",
    help="Environment file containing settings",
    type=click.Path(
        exists=True, readable=True, file_okay=True, dir_okay=False, resolve_path=True
    ),
)
@click.version_option(
    version=__version__,
    message="%(version)s",
    help="Display CLI version",
)
@click.pass_context
def qgis_deployment_toolbelt(
    cli_context: click.Context,
    label: str,
    settings: Path,
    clear: bool,
    verbose: bool,
):
    """Commande parente de SQLite to Airtable.

    \f
    Args:
        cli_context (click.Context): Click context
        label (str): name of run, used to custom some outputs (logs...)
        settings (Path): path to a settings file containing credentials to read database
        clear (bool): option to clear the terminal berfore any other step
        verbose (bool): option to force the verbose mode

    :Example:

        .. code-block:: powershell

            qgis_deployment_toolbelt -c -v -l "Deploy profile" -s "tests/test.conf" check

    """
    # let's be clear or not
    if clear:
        click.clear()

    # -- LOAD CONFIGURATION FILE -------------------------------------------------------
    try:
        conf_dict = {}
        # conf_dict = ConfigurationReader(settings).as_dict_converted
        debug_level = int(conf_dict.get("global").get("debug_level", 0))
        logs_folder = conf_dict.get("global").get("logs_folder", "_logs/")
    except Exception as err:
        exit_cli_error(
            "Problème lors du chargement du fichier de configuration {}"
            " Merci d'exécuter check avant tout autre commande. "
            "Trace: {}".format(settings, err),
            0,
        )
        verbose = 1
        logs_folder = "."

    # -- LOG/VERBOSITY MANAGEMENT ------------------------------------------------------
    # if verbose, override conf value
    if verbose:
        debug_level = 2

    logs_mngr = LogManager(
        debug_level=debug_level,
        label=label,
        folder=Path(logs_folder),
    )
    logs_mngr.headers()
    logger.info("%s mode enabled." % logs_mngr.log_level)

    # end
    logger.info(
        "Main CLI completed after {:5.2f}s.".format(default_timer() - START_TIME)
    )


# -- SUB-COMMANDS ----------------------------------------------------------------------
# Add subcommands to the main command group
qgis_deployment_toolbelt.add_command(cli_check.check)
qgis_deployment_toolbelt.add_command(cli_clean.clean)

# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    # launch cli
    qgis_deployment_toolbelt(obj={})
