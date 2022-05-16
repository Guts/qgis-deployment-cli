#! python3  # noqa: E265

"""
    Main command-line.
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from os import environ
from pathlib import Path
from timeit import default_timer

# 3rd party library
import click

# submodules
from qgis_deployment_toolbelt.__about__ import __version__
from qgis_deployment_toolbelt.commands import cli_check, cli_clean
from qgis_deployment_toolbelt.jobs import JobsOrchestrator
from qgis_deployment_toolbelt.scenarios import ScenarioReader
from qgis_deployment_toolbelt.utils.bouncer import exit_cli_error, exit_cli_normal

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
    "scenario_filepath",
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
    scenario_filepath: Path,
    clear: bool,
    verbose: bool,
):
    """Main command.

    \f
    Args:
        cli_context (click.Context): Click context
        scenario_filepath (Path): path to a scenario file to use
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
    if cli_context.invoked_subcommand is None and Path(scenario_filepath).is_file():
        logger.debug(
            f"Straight run launched using default scenario file: {scenario_filepath}."
        )

        # -- LOAD CONFIGURATION FILE ---------------------------------------------------
        scenario = ScenarioReader(in_yaml=scenario_filepath)

        # Apply log level from scenario (only if verbose mode is disabled)
        if scenario.settings.get("DEBUG") is True and not verbose:
            logger.setLevel(logging.DEBUG)
            for h in logger.handlers:
                h.setLevel(logging.DEBUG)
            logger.info(
                f"{logging.getLevelName(logger.getEffectiveLevel())} mode enabled."
            )

        # Validate scenario
        if (
            scenario.settings.get("SCENARIO_VALIDATION", True) is True
            and not scenario.validate_scenario()[0]
        ):
            exit_cli_error(
                "Scenario validation failed. Please check the scenario file."
                "\nValidation report:\n- {}".format(
                    "\n- ".join(scenario.validate_scenario()[1])
                )
            )

        # Use metadata to inform which scenario is running
        click.echo(
            "Running scenario: {title} ({id}).\n{description}".format(
                **scenario.metadata
            )
        )

        # Set environment vars for the scenario
        for var, value in scenario.settings.items():
            if value is not None:
                logger.debug(f"Setting environment variable {var} = {value}.")
                environ[var] = str(value)
            else:
                logger.debug(f"Ignored None value: {var}.")

        # -- STEPS JOBS
        steps_ok = []
        orchestrator = JobsOrchestrator()

        # filter out unrecognized jobs
        for step in scenario.steps:
            if step.get("uses") not in orchestrator.jobs_ids:
                logger.warning(
                    f"{step.get('uses')} not found in available jobs. Skipping."
                )
                continue
            else:
                steps_ok.append(step)

        # run job
        with click.progressbar(
            steps_ok, label="Running the scenario.."
        ) as progress_bar:
            for step in progress_bar:
                click.secho("Running step: {}".format(step.get("uses")), fg="green")
                try:
                    job = orchestrator.init_job_class_from_id(
                        job_id=step.get("uses"), options=step.get("with")
                    )
                    job.run()
                except Exception as err:
                    exit_cli_error(err)

    # -- ERROR -------------------------------------------------------------------------
    elif cli_context.invoked_subcommand is None and not Path(scenario).is_file():
        exit_cli_error(
            "Straight run launched but no default scenario file found."
            "\nPlease make sure there is a default scenario file `scenario.qdt.yml` "
            f"here {Path(scenario).parent} or use it as a CLI passing the scenario "
            "filepath as an argument."
        )
    else:
        logger.debug(
            f"CLI mode enabled, invoking {cli_context.invoked_subcommand} "
            f"with arguments: {cli_context.args}."
        )
        exit_cli_normal(message="CLI mode enabled", abort=False)

    # end
    logger.debug(
        "Timestamp: {} completed after {:5.2f}s.".format(
            cli_context.info_name, default_timer() - START_TIME
        )
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
