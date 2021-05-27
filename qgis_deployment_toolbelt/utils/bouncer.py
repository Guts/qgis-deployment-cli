#! python3  # noqa: E265

"""
    Shortcuts to exit CLI properly and with pretty messages.

    Author: Julien Moura (github.com/guts)
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging

# 3rd party
import click

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)

# #############################################################################
# ########## Functions #############
# ##################################


def exit_cli_error(message: str, abort: bool = True):
    """Display error message (red) and stop execution.

    :param str message: message to log and display in terminal.
    :param bool abort: option to abort after displaying . Defaults to: True - optional
    """
    # log
    logger.error(message, exc_info=True)

    # handle cases when the full exception is passed
    if isinstance(message, Exception):
        if isinstance(message.args, tuple) and len(message.args):
            message = message.args[0]
        else:
            message = getattr(message, "message", repr(message))

    # echo to terminal
    click.secho(message=message, err=True, fg="red")
    if abort:
        click.Context.abort(message)


def exit_cli_normal(message: str, abort: bool = True):
    """Display normal message (magenta) and stop execution.

    :param str message: message to log and display in terminal.
    :param bool abort: option to abort after displaying . Defaults to: True - optional
    """
    logger.info(message)
    click.secho(message=message, err=False, fg="magenta")

    if abort:
        click.Context.abort(message)


def exit_cli_success(message: str, abort: bool = True):
    """Display success message (green) and stop execution.

    :param str message: message to log and display in terminal.
    :param bool abort: option to abort after displaying the message. Defaults to: True - optional
    """
    logger.info(message)
    click.secho(message=message, err=False, fg="green")
    if abort:
        click.Context.abort(message)


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
