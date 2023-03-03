#! python3  # noqa: E265

"""
    Main command-line.
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import argparse
import logging
from typing import List

# submodules
from qgis_deployment_toolbelt.__about__ import (
    __author__,
    __summary__,
    __title__,
    __title_clean__,
    __uri_homepage__,
    __version__,
)
from qgis_deployment_toolbelt.commands import parser_main_deployment, parser_upgrade

# #############################################################################
# ########## Globals ###############
# ##################################

# ############################################################################
# ########## FUNCTIONS ###########
# ################################


def add_common_arguments(parser_to_update: argparse.ArgumentParser):
    """Apply common argument to an existing parser.

    Args:
        parser_to_update (argparse.ArgumentParser): parser to which arguments need to be added

    Returns:
        argparse.ArgumentParser: parser with added options
    """
    parser_to_update.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=1,
        dest="verbosity",
        help="Niveau de verbosité : None = WARNING, -v = INFO, -vv = DEBUG",
    )
    return parser_to_update


# ############################################################################
# ########## MAIN ################
# ################################
def main(in_args: List[str] = None):
    """Main CLI entrypoint.

    Args:
        in_args (List[str], optional): list of command-line arguments. Defaults to None.
    """
    # create the top-level parser
    main_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Developed by: {__author__}\nDocumentation: {__uri_homepage__}",
        description=f"{__title__} {__version__} - {__summary__}",
    )

    # -- ROOT ARGUMENTS --

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    main_parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=1,
        dest="verbosity",
        help="Verbosity level. None = WARNING, -v = INFO, -vv = DEBUG",
    )

    main_parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help="Display CLI version",
    )

    # -- SUB-COMMANDS --
    subparsers = main_parser.add_subparsers(title="Sub-commands", dest="command")

    # Main logic
    subcmd_deployment = subparsers.add_parser(
        "deploy",
        help="QDT's main logic: run the deployment's scenario.",
        formatter_class=main_parser.formatter_class,
        prog="deployment",
    )
    add_common_arguments(subcmd_deployment)
    parser_main_deployment(subcmd_deployment)

    # Upgrader
    subcmd_upgrade = subparsers.add_parser(
        "upgrade",
        aliases=["auto-update", "update"],
        help="Check if a new version of QDT is available and download it locally.",
        formatter_class=main_parser.formatter_class,
        prog="upgrade",
    )
    add_common_arguments(subcmd_upgrade)
    parser_upgrade(subcmd_upgrade)

    # -- PARSE ARGS --

    # just get passed args
    args = main_parser.parse_args(in_args)

    # set log level depending on verbosity argument
    if 0 < args.verbosity < 4:
        args.verbosity = 40 - (10 * args.verbosity)
    elif args.verbosity >= 4:
        # debug is the limit
        args.verbosity = 40 - (10 * 3)
    else:
        args.verbosity = 0

    logging.basicConfig(
        level=args.verbosity,
        format="%(asctime)s||%(levelname)s||%(module)s||%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler()
    console.setLevel(args.verbosity)

    # add the handler to the root logger
    logger = logging.getLogger(__title_clean__)
    logger.debug(f"Log level set: {logging.getLevelName(args.verbosity)}")

    # -- RUN LOGIC --
    if hasattr(args, "func"):
        args.func(args)
    else:
        # if no args, run deployment
        main(["deploy"])


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    # launch cli
    main()  # required by unittest
