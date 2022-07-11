#! python3  # noqa: E265

"""
    Sub-command in charge of cleaning up temporary files.

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
from send2trash import send2trash

# submodules
from qgis_deployment_toolbelt.utils.bouncer import exit_cli_success

# #############################################################################
# ########## Globals ###############
# ##################################

# chronometer
START_TIME = default_timer()

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ####### Command-line ############
# #################################
@click.command(name="clean")
@click.option(
    "-d",
    "--days-older",
    help="Number of days after which the file is deleted.",
    default=30,
    show_default=True,
    type=click.INT,
    envvar="QGIS_DEPLOYMENT_CLEAN_DAYS_OLDER",
)
@click.option(
    "-e",
    "--remove-empty-folders",
    help="Remove empty folders.",
    is_flag=True,
    default=True,
    show_default=True,
)
@click.pass_context
def clean(
    cli_context: click.Context, days_older: int, remove_empty_folders: bool
) -> None:
    """Delete logs and output folders older than the frequency set in the \
    configuration: `CLEAN_FREQUENCY`.

    \f
    :param click.core.Context cli_context: Click context
    :param int days_older: number of days after which the file is deleted.
    :param bool remove_empty_folders: if passed, empty folders will be deleted too
    """
    logger.info("CLEAN started after {:5.2f}s.".format(default_timer() - START_TIME))

    # extract values from CLI context
    logs_folder = Path("./_logs/")
    if not logs_folder.exists():
        exit_cli_success(f"No logs to clean in: {logs_folder.resolve()}", abort=True)

    date_ref_days_ago = datetime.now() - timedelta(days=days_older)

    # logs folder
    li_folders_logs = Path(logs_folder).iterdir()

    # go deleting
    with click.progressbar(
        list(li_folders_logs),
        label="Removing log folders",
    ) as log_folders:
        for subobj in log_folders:
            # compare last modification date
            if datetime.fromtimestamp(subobj.stat().st_mtime) < date_ref_days_ago:
                logger.debug(
                    "CLEANER - LOGS - Detected folder/file outdated: {}".format(subobj)
                )
                try:
                    send2trash(str(subobj.resolve()))
                except Exception as e:
                    logger.warning(
                        "Unable to delete: {}. Original error: {}".format(
                            subobj.resolve(), e
                        )
                    )
            # handle empty folders
            if (
                remove_empty_folders
                and subobj.is_dir()
                and not list(subobj.glob("**/*"))
            ):
                logger.info(
                    "Empty folder spotted: {}. Sending it to the trash...".format(
                        str(subobj.resolve())
                    )
                )
                try:
                    send2trash(str(subobj.resolve()))
                except Exception as e:
                    logger.warning(
                        "Unable to delete: {}. Original error: {}".format(
                            subobj.resolve(), e
                        )
                    )

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
    clean(obj={})
