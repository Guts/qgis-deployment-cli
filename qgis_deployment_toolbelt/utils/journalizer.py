#! python3  # noqa: E265

"""Helper to configure logging depending on CLI options."""

# ############################################################################
# ########## IMPORTS #############
# ################################

# standard library
import logging
from getpass import getuser
from logging.handlers import RotatingFileHandler
from os import getenv
from os.path import expanduser, expandvars
from pathlib import Path
from platform import architecture
from platform import platform as opersys
from socket import gethostname

# package
from qgis_deployment_toolbelt.__about__ import __title__, __version__
from qgis_deployment_toolbelt.constants import get_qdt_working_directory
from qgis_deployment_toolbelt.utils.check_path import check_path
from qgis_deployment_toolbelt.utils.proxies import get_proxy_settings

# ############################################################################
# ########## GLOBALS #############
# ################################

# logs
logger = logging.getLogger(__name__)

# ############################################################################
# ########## FUNCTIONS ###########
# ################################


def configure_logger(verbosity: int = 1, logfile: Path = None):
    """Configure logging according to verbosity from CLI.

    Args:
        verbosity (int): verbosity level
        logfile (Path, optional): file where to store log. Defaults to None.
    """
    # handle log level overridden by environment variable
    verbosity = getenv("QDT_LOGS_LEVEL", verbosity)
    try:
        verbosity = int(verbosity)
    except ValueError as err:
        logger.error(f"Bad verbosity value type: {err}. Fallback to 1.")
        verbosity = 1

    # set log level depending on verbosity argument
    if 0 < verbosity < 4:
        verbosity = 40 - (10 * verbosity)
    elif verbosity >= 4:
        # debug is the limit
        verbosity = 40 - (10 * 3)
    else:
        verbosity = 0

    # set console handler
    log_console_handler = logging.StreamHandler()
    log_console_handler.setLevel(verbosity)

    # set log file
    if not logfile:
        logging.basicConfig(
            level=verbosity,
            format="%(asctime)s||%(levelname)s||%(module)s||%(lineno)d||%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[log_console_handler],
        )

    else:
        if getenv("QDT_LOGS_DIR") and check_path(
            input_path=Path(expandvars(expanduser(getenv("QDT_LOGS_DIR")))),
            must_be_a_file=False,
            must_be_a_folder=True,
            must_be_writable=True,
            raise_error=False,
        ):
            logs_folder = Path(expandvars(expanduser(getenv("QDT_LOGS_DIR"))))
            logger.debug(
                f"Logs folder set with QDT_LOGS_DIR environment variable: {logs_folder}"
            )
        else:
            logs_folder = get_qdt_working_directory().parent / "logs"
            logger.debug(
                "Logs folder specified in QDT_LOGS_DIR environment variable "
                f"{getenv('QDT_LOGS_DIR')} can't be used (see logs above). Fallback on "
                f"default folder: {logs_folder}"
            )

        # make sure folder exists
        logs_folder.mkdir(exist_ok=True, parents=True)
        logs_filepath = Path(logs_folder, logfile)

        log_file_handler = RotatingFileHandler(
            backupCount=10,
            delay=True,
            encoding="UTF-8",
            filename=logs_filepath,
            maxBytes=3000000,
            mode="a",
        )
        # force new file by execution
        if logs_filepath.is_file():
            log_file_handler.doRollover()

        logging.basicConfig(
            level=verbosity,
            format="%(asctime)s||%(levelname)s||%(module)s||%(lineno)d||%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[log_console_handler, log_file_handler],
        )

        logger.info(f"Log file: {logs_filepath}")

    headers()


def headers():
    """Basic information to log before other message."""
    # initialize the log
    logger.info(f"{'='*10} {__title__} - {__version__} {'='*10}")
    logger.debug(f"Operating System: {opersys()}")
    logger.debug(f"Architecture: {architecture()[0]}")
    logger.debug(f"Computer: {gethostname()}")
    logger.debug(f"Launched by user: {getuser()}")

    if getenv("userdomain"):
        logger.debug(f"OS Domain: {getenv('userdomain')}")

    if get_proxy_settings():
        logger.debug(f"Network proxies detected: {get_proxy_settings()}")
    else:
        logger.debug("No network proxies detected")
