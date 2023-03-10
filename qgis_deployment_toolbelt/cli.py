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
import sys

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
from qgis_deployment_toolbelt.utils.journalizer import configure_logger

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


def set_default_subparser(
    parser_to_update: argparse.ArgumentParser,
    default_subparser_name: str,
    args: list = None,
):
    """Set a default subparser to a parent parser. Call after setup and just before
        parse_args().
        See: <https://stackoverflow.com/questions/5176691/argparse-how-to-specify-a-default-subcommand>

    Args:
        parser_to_update (argparse.ArgumentParser): parent parser to add
        default_subparser_name (str): name of the subparser to call by default
        args (list, optional): if set is the argument list handed to parse_args().
        Defaults to None.
    """
    subparser_found = False
    for arg in sys.argv[1:]:
        if arg in [
            "-h",
            "--help",
            "--version",
            "--no-logfile",
        ]:  # ignore main parser args
            break

    else:
        for x in parser_to_update._subparsers._actions:
            if not isinstance(x, argparse._SubParsersAction):
                continue
            for sp_name in x._name_parser_map.keys():
                if sp_name in sys.argv[1:]:
                    subparser_found = True
        if not subparser_found:
            # insert default in first position, this implies no
            # global options without a sub_parsers specified
            if args is None:
                sys.argv.insert(1, default_subparser_name)
            else:
                args.insert(0, default_subparser_name)


# ############################################################################
# ########## MAIN ################
# ################################
def main(in_args: list[str] = None):
    """Main CLI entrypoint.

    Args:
        in_args (List[str], optional): list of command-line arguments. Defaults to None.
    """
    # create the top-level parser
    main_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Developed by: {__author__}\nDocumentation: {__uri_homepage__}",
        description=f"{__title__} {__version__} - {__summary__}",
        argument_default=argparse.SUPPRESS,
    )

    # -- ROOT ARGUMENTS --

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    main_parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=1,
        dest="verbosity",
        help="Verbosity level. None = WARNING, -v = INFO, -vv = DEBUG. Can be set with "
        "QDT_LOGS_LEVEL environment variable and logs location with QDT_LOGS_DIR.",
    )

    main_parser.add_argument(
        "--no-logfile",
        default=True,
        action="store_false",
        dest="opt_logfile_disabled",
        help="Disable log file. Log files are usually created, rotated and stored in the"
        "folder set by QDT_LOGS_DIR.",
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
    set_default_subparser(parser_to_update=main_parser, default_subparser_name="deploy")

    # just get passed args
    args = main_parser.parse_args(in_args)

    # log configuration
    if args.opt_logfile_disabled:
        configure_logger(
            verbosity=args.verbosity, logfile=f"{__title_clean__}_{__version__}.log"
        )
    else:
        configure_logger(verbosity=args.verbosity)

    # add the handler to the root logger
    logger = logging.getLogger(__title_clean__)
    logger.debug(f"Log level set: {logging.getLevelName(args.verbosity)}")

    # -- RUN LOGIC --
    if hasattr(args, "func"):
        args.func(args)


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    # launch cli
    main()  # required by unittest
