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

# default CLI context.
# See: https://click.palletsprojects.com/en/7.x/commands/#context-defaults
CONTEXT_SETTINGS = dict(obj={})


# #############################################################################
# ####### Command-line ############
# #################################
@click.command(name="clean")
@click.option(
    "-rm",
    "--remove-empty-folders",
    help="Remove empty folders.",
    is_flag=True,
    default=True,
    show_default=True,
)
@click.pass_context
def clean(cli_context: click.Context, remove_empty_folders: bool):
    """Delete logs and output folders older than the frequency set in the \
    configuration: `CLEAN_FREQUENCY`.

    \f
    :param click.core.Context cli_context: Click context
    :param bool remove_empty_folders: if passed, empty folders will be deleted too
    """
    logger.info("CLEAN started after {:5.2f}s.".format(default_timer() - START_TIME))

    # extract values from CLI context
    logs_folder = cli_context.obj.get("FOLDER_LOGS")
    config_dict = cli_context.obj.get("SETTINGS_DICT")

    logger.info(
        "Suppression des fichiers antérieurs à {} jours.".format(
            config_dict.get("global").get("clean_frequency_days")
        )
    )
    date_ref_days_ago = datetime.now() - timedelta(
        days=int(config_dict.get("global").get("clean_frequency_days"))
    )

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
