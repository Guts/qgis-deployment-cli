#! python3  # noqa: E265

"""
    Log management.

    Author: Julien Moura (github.com/guts)

    See: https://docs.python.org/fr/3/howto/logging.html
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from getpass import getuser
from logging.handlers import RotatingFileHandler
from os import environ
from pathlib import Path
from platform import architecture
from platform import platform as opersys
from socket import gethostname

# modules
from qgis_deployment_toolbelt.__about__ import __title__
from qgis_deployment_toolbelt.__about__ import __title_clean__ as package_name
from qgis_deployment_toolbelt.__about__ import __version__
from qgis_deployment_toolbelt.utils.bouncer import exit_cli_error

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################


class LogManager:
    """Manage logs: configuration, parsing, etc."""

    LOG_FORMAT = logging.Formatter(
        "%(asctime)s || %(levelname)s "
        "|| %(module)s - %(lineno)d ||"
        " %(funcName)s || %(message)s"
    )

    def __init__(
        self,
        debug_level: int = 0,
        label: str = package_name,
        folder: Path = Path("./_logs"),
    ):
        """Instanciation method."""
        self.debug_level = debug_level
        self.folder = Path(folder)
        self.label = "".join(e for e in label if e.isalnum())

        if debug_level == 2:
            self.console_level = logging.DEBUG
            self.file_level = logging.DEBUG
            self.log_level = "DEBUG"
        elif debug_level == 1:
            self.console_level = logging.INFO
            self.file_level = logging.INFO
            self.log_level = "INFORMATIVE"
        else:
            self.console_level = logging.WARNING
            self.file_level = logging.INFO
            self.log_level = "LIGHT"

        # ensure folder is created
        try:
            folder.mkdir(exist_ok=True, parents=True)
        except PermissionError as err:
            msg_err = (
                "Impossible to create the logs folder. Does the user '{}' ({}) have "
                "write permissions on: {}. Trace: {}"
            ).format(environ.get("userdomain"), getuser(), folder, err)
            exit_cli_error(msg_err)
        self.folder = folder

        # create logger
        self.initial_logger_config()

    def initial_logger_config(self) -> logging.Logger:
        """Configure root logger. \
        BE CAREFUL: it depends a lot of how click implemented logging facilities. \
        So, sadly, every option is not available.

        :return: configured logger
        :rtype: logging.Logger
        """
        #  create main logger
        logging.captureWarnings(False)
        logger = logging.getLogger()
        logger.setLevel(self.console_level)

        # create console handler - seems to be ignored by click
        log_console_handler = logging.StreamHandler()
        log_console_handler.setLevel(self.console_level)

        # create file handler
        log_file_handler = RotatingFileHandler(
            filename=self.folder / "{}.log".format(self.label),
            mode="a",
            maxBytes=3000000,
            backupCount=10,
            encoding="UTF-8",
        )
        log_file_handler.setLevel(self.file_level)

        # apply format
        log_file_handler.setFormatter(self.LOG_FORMAT)

        # add only file handler to the logger, to avoid duplicated messages
        # logger.addHandler(log_console_handler)
        logger.addHandler(log_file_handler)

        return logger

    def headers(self):
        """Basic information to log before other message."""
        # initialize the log
        logger.info("===== {} - Version {} =====".format(__title__, __version__))
        logger.info("Operating System: {}".format(opersys()))
        logger.info("Architecture: {}".format(architecture()[0]))
        logger.info("Computer: {}".format(gethostname()))
        logger.info("Launched by: {}".format(getuser()))
        logger.info("OS Domain: {}".format(environ.get("userdomain")))


# #############################################################################
# ##### Main #######################
# ##################################
if __name__ == "__main__":
    pass
