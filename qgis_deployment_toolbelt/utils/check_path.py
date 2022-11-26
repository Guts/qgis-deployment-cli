#! python3  # noqa: E265

"""
    Helpers to check file: readable, exists, etc..

    Author: Julien Moura (https://github.com/guts)
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from os import R_OK, W_OK, access
from pathlib import Path
from typing import Union

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)

# #############################################################################
# ########## Functions #############
# ##################################


def check_var_can_be_path(input_var: str, raise_error: bool = True) -> bool:
    """Check is the path can be converted as pathlib.Path.

    Args:
        input_var (str): var to check
        raise_error (bool, optional): if True, it raises an exception. Defaults to True.

    Raises:
        TypeError: if input path can't be converted and raise_error is False

    Returns:
        bool: True if the input can be converted to pathlib.Path
    """
    try:
        input_var = Path(input_var)
        return True
    except Exception as exc:
        error_message = f"Converting {input_var} into Path failed. Trace: {exc}"
        if raise_error:
            raise TypeError(error_message)
        else:
            logger.error(error_message)
            return False


def check_path_exists(input_path: Union[str, Path], raise_error: bool = True) -> bool:
    """Check if the input path (file or folder) exists.

    Args:
        input_path (Union[str, Path]): path to check
        raise_error (bool, optional): if True, it raises an exception. Defaults to True.

    Raises:
        FileExistsError: if the path doesn't exist and raise_error is False

    Returns:
        bool: True if the path exists.
    """
    if not isinstance(input_path, Path):
        if (
            not check_var_can_be_path(input_path, raise_error=raise_error)
            and not raise_error
        ):
            return False
        # if previous check passed, let's convert it safely
        input_path = Path(input_path)
    if not input_path.exists():
        error_message = f"{input_path.resolve()} doesn't exist."
        if raise_error:
            raise FileExistsError(error_message)
        else:
            logger.error(error_message)
            return False
    else:
        return True


def check_path_is_readable(input_path: Path, raise_error: bool = True) -> bool:
    """Check if the input path (file or folder) is readable.

    Args:
        input_path (Path): path to check
        raise_error (bool, optional): if True, it raises an exception. Defaults to True.

    Raises:
        FileExistsError: if the path is not readable and raise_error is False

    Returns:
        bool: True if the path is readable.
    """
    # firstly check the path is valid and exists
    if not isinstance(input_path, Path):
        if (
            not check_path_exists(input_path, raise_error=raise_error)
            and not raise_error
        ):
            return False
        # if previous check passed, let's convert it safely
        input_path = Path(input_path)

    if not access(input_path, R_OK):
        error_message = f"{input_path.resolve()} isn't readable."
        if raise_error:
            raise IOError(error_message)
        else:
            logger.error(f"{input_path.resolve()} isn't readable.")
            return False
    else:
        return True


def check_path_is_writable(input_path: Path, raise_error: bool = True) -> bool:
    """Check if the input path (file or folder) is writable.

    Args:
        input_path (Path): path to check
        raise_error (bool, optional): if True, it raises an exception. Defaults to True.

    Raises:
        FileExistsError: if the path is not writable and raise_error is False

    Returns:
        bool: True if the path is writable.
    """
    # firstly check the path is valid and exists
    if not isinstance(input_path, Path):
        if (
            not check_path_exists(input_path, raise_error=raise_error)
            and not raise_error
        ):
            return False
        # if previous check passed, let's convert it safely
        input_path = Path(input_path)

    if not access(input_path, W_OK):
        error_message = f"{input_path.resolve()} isn't writable."
        if raise_error:
            raise IOError(error_message)
        else:
            logger.error(error_message)
            return False
    else:
        return True


def check_path(
    input_path: Union[str, Path],
    must_exists: bool = True,
    must_be_readable: bool = True,
    must_be_writable: bool = False,
    must_be_a_folder: bool = False,
    must_be_a_file: bool = False,
    raise_error: bool = True,
) -> bool:
    """Meta function of the module. Check if a given path complies with some constraints.

    Args:
        input_path (Union[str, Path]): path to check
        must_exists (bool, optional): path must exist. Defaults to True.
        must_be_readable (bool, optional): path must be readable. Defaults to True.
        must_be_writable (bool, optional): path must be writable. Defaults to False.
        must_be_a_folder (bool, optional): path must be a folder. Mutually exclusive \
            with must_be_a_file. Defaults to False.
        must_be_a_file (bool, optional): path must be a file. Mutually exclusive with \
            must_be_a_folder. Defaults to False.
        raise_error (bool, optional): if True, it raises an exception. Defaults to True.

    Raises:
        ValueError: if must_be_a_file and must_be_a_folder are both set to True
        FileNotFoundError: if the path is not a file and must_be_a_file is set to True
        NotADirectoryError: if the path is not a folder and must_be_a_folder is set to True

    Returns:
        bool:  True if the path complies with constraints.
    """
    # check arguments
    if all([must_be_a_file, must_be_a_folder]):
        raise ValueError(
            "These options are mutually exclusive: must_be_a_file, must_be_a_folder"
        )

    # check input path if usable with pathlib.Path
    if not isinstance(input_path, Path):
        check_var = check_var_can_be_path(input_var=input_path, raise_error=raise_error)
        if not check_var and not raise_error:
            return False
        input_path = Path(input_path)

    # check
    if must_exists:
        check_exist = check_path_exists(input_path=input_path, raise_error=raise_error)
        if not check_exist and not raise_error:
            return False

    # check file or folder
    if must_be_a_file and not input_path.is_file():
        error_message = f"{input_path.resolve()} is not a file."
        if raise_error:
            raise FileNotFoundError(error_message)
        else:
            logger.error(error_message)
            return False
    if must_be_a_folder and not input_path.is_dir():
        error_message = f"{input_path.resolve()} is not a folder."
        if raise_error:
            raise NotADirectoryError(error_message)
        else:
            logger.error(error_message)
            return False

    # check chmod
    if must_be_readable:
        check_readable = check_path_is_readable(
            input_path=input_path, raise_error=raise_error
        )
        if not check_readable and not raise_error:
            return False

    if must_be_writable:
        check_writable = check_path_is_writable(
            input_path=input_path, raise_error=raise_error
        )
        if not check_writable and not raise_error:
            return False

    return True


# ############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
