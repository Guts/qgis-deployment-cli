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
from qgis_deployment_toolbelt.commands import cli_check, cli_clean, cli_upgrade
from qgis_deployment_toolbelt.constants import get_qdt_working_directory
from qgis_deployment_toolbelt.jobs import JobsOrchestrator
from qgis_deployment_toolbelt.scenarios import ScenarioReader
from qgis_deployment_toolbelt.utils.bouncer import exit_cli_error, exit_cli_normal

# #############################################################################
# ########## Globals ###############
# ##################################

# chronometer
START_TIME = default_timer()

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
@click.option(
    "--disable-validation",
    "disable_validation",
    is_flag=True,
    show_default=True,
    help="Disable the validation of the scenario",
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
    disable_validation: bool,
    clear: bool,
    verbose: bool,
):
    """Main command.

    \f
    Args:
        cli_context (click.Context): Click context
        scenario_filepath (Path): path to a scenario file to use
        disable_validation (bool): option to disable the validation of the scenario
        clear (bool): option to clear the terminal berfore any other step
        verbose (bool): option to force the verbose mode

    :Example:

        .. code-block:: powershell

            qgis-deployment-toolbelt --disable_validation -c --verbose check

    """
    scenario = None
    result_scenario_validity = None

    # -- LOAD CONFIGURATION FILE ---------------------------------------------------
    if Path(scenario_filepath).is_file():
        scenario = ScenarioReader(in_yaml=scenario_filepath)
        scenario_validity = scenario.validate_scenario()
        if not scenario_validity[0]:
            result_scenario_validity = (
                "Scenario validation failed. Please check the scenario file."
                "\nValidation report:\n- {}".format("\n- ".join(scenario_validity[1]))
            )

    # Check the validity of the scenario
    if not disable_validation and scenario is not None:
        if result_scenario_validity is not None:
            exit_cli_error(result_scenario_validity)

    # -- LOG/VERBOSITY MANAGEMENT ------------------------------------------------------
    # if verbose, override conf value
    if verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.WARNING

    logging.basicConfig(
        format="[%(levelname)s] %(message)s",
        level=log_level,
    )
    logger = logging.getLogger(__name__)
    logger.info(f"{logging.getLevelName(logger.getEffectiveLevel())} mode enabled.")

    click.echo(
        "Timestamp: {} started after {:5.2f}s.".format(
            cli_context.info_name, default_timer() - START_TIME
        )
    )

    # -- USING DEFAULT SCENARIO OR NOT -------------------------------------------------
    if cli_context.invoked_subcommand is None and scenario is not None:
        logger.debug(
            f"Straight run launched using default scenario file: {scenario_filepath}."
        )

        # Check the validity of the scenario
        if result_scenario_validity is not None:
            exit_cli_error(result_scenario_validity)

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

        logger.info(
            f"QDT working folder: {get_qdt_working_directory(specific_value=scenario.settings.get('LOCAL_QDT_WORKDIR'), identifier=scenario.metadata.get('id'))}"
        )

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
    elif cli_context.invoked_subcommand is None and scenario is None:
        exit_cli_error(
            "Straight run launched but no default scenario file found."
            "\nPlease make sure there is a default scenario file `scenario.qdt.yml` "
            f"here {Path(scenario_filepath).parent} or use it as a CLI passing the scenario "
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
qgis_deployment_toolbelt.add_command(cli_upgrade.upgrade)

# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    # launch cli
    qgis_deployment_toolbelt(obj={})
