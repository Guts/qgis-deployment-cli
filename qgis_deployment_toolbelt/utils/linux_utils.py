#! python3  # noqa: E265

"""
    Utilities specific for Linux.

    Author: Julien Moura (https://github.com/guts)

"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard
import logging
import os
import re
from functools import lru_cache
from os import getenv
from pathlib import Path

# 3rd party
import shellingham

# project
from qgis_deployment_toolbelt.utils.check_path import check_path

# #############################################################################
# ########## Globals ###############
# ##################################

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s||%(levelname)s||%(module)s||%(lineno)d||%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

qdt_block_comment_start = "# BEGIN QDT MANAGED BLOCK"
qdt_block_comment_end = "# END QDT MANAGED BLOCK"
shell_path_to_names = {
    "bash": ("/bin/bash", "/usr/bin/bash"),
    "zsh": ("/bin/bash/zsh", "/usr/bin/zsh"),
}

# #############################################################################
# ########## Functions #############
# ##################################


@lru_cache
def find_key_from_values(value_to_find: str) -> str | None:
    """Finds the key corresponding to a given value in a dictionary where values are
    tuples.

    Args:
        value_to_find (str): The value to search for in the dictionary values.

    Returns:
        str | None: The key corresponding to the found value. Returns None if the value
            is not found.
    """
    for key, values in shell_path_to_names.items():
        if value_to_find in values:
            return key
    return None


def get_shell_to_use() -> tuple[str, str] | None:
    try:
        shell = shellingham.detect_shell()
        logger.debug(f"Detected active shell: {shell}")
    except shellingham.ShellDetectionFailure as exc:
        logger.warning(
            "Failed to detect active shell. Using default from environment "
            f"variable. Trace: {exc}"
        )
        if os.name == "posix":
            if shell_path := getenv("SHELL"):
                shell_name = find_key_from_values(value_to_find=getenv("SHELL"))
                if shell_name:
                    return (shell_name, shell_path)
            return None
        elif os.name == "nt":
            return getenv("COMSPEC")
        else:
            raise NotImplementedError(f"OS {os.name!r} support not available")

        logger.debug(f"Default shell from environment variable: {shell}")

    return shell


def is_dot_profile_file() -> bool:
    return check_path(
        input_path=Path.home().joinpath(".profile"),
        must_be_a_file=True,
        must_exists=True,
        raise_error=False,
    )


def get_environment_variable(envvar_name: str, scope: str = "user") -> str | None:
    """Get environment variable from Linux profile file
    Args:

        envvar_name (str): environment variable name (= key) to retrieve
        scope (str, optional): environment variable scope. Must be "user" or "system",
            defaults to "user". Defaults to "user".

    Returns:
        Optional[str]: environment variable value or None if not found
    """

    profile_file = get_profile_file(scope)

    logger.debug(f"parsing {profile_file}")

    # Read file content
    with profile_file.open(mode="r", encoding="UTF-8") as file:
        lines = file.readlines()

    # look for export line
    env_value = None
    for line in lines:
        if envvar_name in line.strip():
            env_value = [item.strip() for item in re.split("=", line)][-1]

    logger.debug(f"Value for environment variable {envvar_name}: {env_value}")

    return env_value


def set_environment_variable(
    env_key: str, env_value: str | bool | int, scope: str = "user"
) -> bool:
    """Set environment variable in Linux profile file
    Args:

        env_key (str): environment variable name (= key) to set
        env_value (str): environment variable value to set
        scope (str, optional): environment variable scope. Must be "user" or "system",
            defaults to "user". Defaults to "user".

    Returns:
        Optional[str]: environment variable value or None if not found
    """

    if isinstance(env_value, bool):
        env_value = str(bool(env_value)).lower()

    """
    shell: tuple[str, str] | None = get_shell_to_use()
    if shell is None:
        logger.error("Shell to use is not recognized.")
        return False
    """

    if get_environment_variable(env_key, scope) is not None:
        logger.info(f"Environment variable {env_key} already there")
        if get_environment_variable(env_key, scope) != env_value:
            logger.info("Environment variable value to be changed")
            delete_environment_variable(env_key)
        else:
            logger.info(f"Environment variable already set to {env_value}")
            return True

    bash_profile = get_profile_file(scope)

    # if shell[0] == "bash":
    if bash_profile is not None:
        """
        bash_profile = Path.home().joinpath(".profile")
        if not is_dot_profile_file():
            logger.error(
                f"Shell profile does not exist and will be created {bash_profile}"
            )
            bash_profile.touch()
        """

        logger.debug(f"parsing {bash_profile}")

        export_line = f"export {env_key}={str(env_value)}"
        block_start_found = False
        block_end_found = False
        block_end_line: int = 0
        line_found = False

        # Read file content
        with bash_profile.open(mode="r", encoding="UTF-8") as file:
            lines = file.readlines()

        # look for block and export line
        line_number: int = 0
        for line in lines:
            if line.strip() == qdt_block_comment_start:
                block_start_found = True
            elif line.strip() == qdt_block_comment_end:
                block_end_found = True
                block_end_line = line_number
            elif line.strip() == export_line:
                line_found = True
            # line counter
            line_number += 1

        # check if block exist
        block_found = all([block_start_found, block_end_found])

        if line_found:
            logger.debug(
                f"Environment variable and key {env_key}={env_value} is already present"
            )
            return True
        elif block_found and not line_found:
            lines.insert(block_end_line, f"{export_line}\n")

            with bash_profile.open(mode="w", encoding="UTF-8") as file:
                file.writelines(lines)
            logger.info(
                f"QDT block was already here but not the line: '{export_line}. "
                "It has been added."
            )
            return True
        elif not block_found and not line_found:
            new_lines = (
                f"\n{qdt_block_comment_start}\n",
                f"{export_line}\n",
                f"{qdt_block_comment_end}",
            )
            with open(bash_profile, "a") as file:
                file.writelines(new_lines)
            logger.info(
                f"Nor QDT block and the line: '{export_line}' were present. "
                "Both have been added."
            )
            return True
    else:
        logger.error(f"Shell {shell[0]} is not supported")
        return False


"""
def update_environment_variable(env_key: str, env_value: str | bool | int, scope: str = "user") -> bool:
    # TODO don't add an extra line
    # TODO integrate in set_environment_variable : delete if exists
    resdel: bool = delete_environment_variable(env_key, scope)
    resadd: bool = set_environment_variable(env_key, env_value, scope)
    logger.info(
        f"Environment variable {env_key} has been updated to {env_value}\n"
        "Shell profile updated"
    )

    return resdel and resadd
"""


def delete_environment_variable(env_key: str, scope: str = "user") -> bool:
    """Remove environment variable from Linux profile file
    Args:

        env_key (str): environment variable name (= key) to remove
        scope (str, optional): environment variable scope. Must be "user" or "system",
            defaults to "user". Defaults to "user".

    Returns:
        [bool]: true if environment variable was successfully removed
                false if not
    """

    """
    shell: tuple[str, str] | None = get_shell_to_use()

    if shell is None:
        logger.error("Shell to use is not recognized.")
        return False
    """

    bash_profile = get_profile_file(scope)

    # if shell[0] == "bash":
    if bash_profile is not None:
        """
        bash_profile = Path.home().joinpath(".profile")
        if not is_dot_profile_file():
            logger.error(
                f"Shell profile does not exist {bash_profile}"
            )
            return False
        """

        logger.debug(f"parsing {bash_profile}")

        line_begin = f"export {env_key}="
        block_start_found = False
        block_start_line: int = 0
        block_end_found = False
        block_end_line: int = 0
        line_found = False
        line_begin_line: int = 0

        # Lire le contenu du fichier
        with bash_profile.open(mode="r", encoding="UTF-8") as file:
            lines = file.readlines()

        # look for block and beginning of line
        line_number: int = 0
        for line in lines:
            if line.strip() == qdt_block_comment_start:
                block_start_found = True
                block_start_line = line_number
            elif line.strip() == qdt_block_comment_end:
                block_end_found = True
                block_end_line = line_number
            elif line_begin in line.strip():
                line_found = True
                line_begin_line = line_number
            # line counter
            line_number += 1

        # check if block exist
        all([block_start_found, block_end_found])

        pos = []
        if line_found:
            pos.append(line_begin_line)
            logger.debug(
                f"Environment variable and key {env_key} was found. "
                "It will be removed"
            )
        if block_start_found:
            pos.append(block_start_line)
            logger.debug(
                f"QDT block start was found for '{env_key}'. "
                "Block start will be removed."
            )
        if block_end_found:
            pos.append(block_end_line)
            logger.info(
                f"QDT block end was found for: '{env_key}'. "
                "Block end will be removed."
            )
        # pos = [block_start_line, line_begin_line, block_end_line]
        new_lines = [lines[i] for i, e in enumerate(lines) if i not in pos]
        with bash_profile.open(mode="w", encoding="UTF-8") as file:
            file.writelines(new_lines)
        logger.info(
            f"QDT block for environment variable '{env_key}' has been removed. "
            "Shell profile updated."
        )
        return True

    else:
        logger.error(f"Shell {shell[0]} is not supported")
        return False


def get_profile_file(scope: str = "user") -> str:
    """Get Linux profile file depending on shell and scope
    Args:

        scope (str, optional): environment variable scope. Must be "user" or "system",
            defaults to "user". Defaults to "user".

    Returns:
        Optional[str]: profile file path or None if not found
    """

    # TODO : Add shell checking ?
    if scope == "system":
        if check_path(
            input_path=Path("/etc").joinpath("profile"),
            must_be_a_file=True,
            must_exists=True,
            raise_error=False,
        ):
            logger.info("/etc/profile was found and will be used")
            return Path("/etc").joinpath("profile")
        else:
            logger.info("/etc/profile was not found, it will be created and used")
            # Path('/etc').joinpath('profile').touch()
            return Path("/etc").joinpath("profile")

    elif scope == "user":
        if check_path(
            input_path=Path.home().joinpath(".bash_profile"),
            must_be_a_file=True,
            must_exists=True,
            raise_error=False,
        ):
            logger.info("~/.bash_profile was found and will be used")
            return Path.home().joinpath(".bash_profile")
        elif check_path(
            input_path=Path.home().joinpath(".login_profile"),
            must_be_a_file=True,
            must_exists=True,
            raise_error=False,
        ):
            logger.info("~/.login_profile was found and will be used")
            return Path.home().joinpath(".login_profile")
        elif check_path(
            input_path=Path.home().joinpath(".profile"),
            must_be_a_file=True,
            must_exists=True,
            raise_error=False,
        ):
            logger.info("~/.profile was found and will be used")
            return Path.home().joinpath(".profile")
        else:
            logger.info(
                "Neither .bash_profile nor .login_profile nor .profile was found, "
                "~/.profile will be created and used"
            )
            bash_profile.touch()
            return Path.home().joinpath(".profile")
    else:
        logger.error(f"Scope {scope} not handled.")
        return None


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""

    print("User profile file :", get_profile_file("user"))
    print("System profile file :", get_profile_file("system"))

    set_environment_variable("TEST_PERSISTENT_ENVIRONMENT_VARIABLE", False)
    # update_environment_variable("TEST_PERSISTENT_ENVIRONMENT_VARIABLE", False)
    # delete_environment_variable("TEST_PERSISTENT_ENVIRONMENT_VARIABLE")
