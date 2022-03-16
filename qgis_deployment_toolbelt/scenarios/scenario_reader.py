#! python3  # noqa: E265

"""
    Read and validate scenario files.

    Author: Julien Moura (https://github.com/guts, Oslandia)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging
from io import BufferedIOBase
from os import R_OK, access
from pathlib import Path
from typing import Union

# 3rd party
import yaml

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ########## Classes ###############
# ##################################


class ScenarioReader:
    """Read and validate scenario files."""

    def __init__(self, in_yaml: Union[str, Path, BufferedIOBase]):
        """Instanciating Isogeo Metadata YAML Reader."""
        # check and get YAML path
        if isinstance(in_yaml, (str, Path)):
            self.input_yaml = self.check_yaml_file(in_yaml)
            # extract data from input file
            with self.input_yaml.open(mode="r") as bytes_data:
                self.yaml_data = yaml.safe_load(bytes_data)
        elif isinstance(in_yaml, BufferedIOBase):
            self.input_yaml = self.check_yaml_buffer(in_yaml)
            # extract data from input file
            self.yaml_data = yaml.safe_load(self.input_yaml)
        else:
            raise TypeError

    # CHECKS
    def check_yaml_file(self, yaml_path: Union[str, Path]) -> Path:
        """Perform some checks on passed yaml file and load it as Path object.

        :param yaml_path: path to the yaml file to check

        :returns: sanitized yaml path
        :rtype: Path
        """
        # if path as string load it in Path object
        if isinstance(yaml_path, str):
            try:
                yaml_path = Path(yaml_path)
            except Exception as exc:
                raise TypeError("Converting yaml path failed: {}".format(exc))

        # check if file exists
        if not yaml_path.exists():
            raise FileExistsError(
                "YAML file to check doesn't exist: {}".format(yaml_path.resolve())
            )

        # check if it's a file
        if not yaml_path.is_file():
            raise IOError("YAML file is not a file: {}".format(yaml_path.resolve()))

        # check if file is readable
        if not access(yaml_path, R_OK):
            raise IOError("yaml file isn't readable: {}".format(yaml_path))

        # check integrity and structure
        with yaml_path.open(mode="r") as in_yaml_file:
            try:
                yaml.safe_load_all(in_yaml_file)
            except yaml.YAMLError as exc:
                logger.error(msg="YAML file is invalid: {}".format(yaml_path.resolve()))
                raise exc
            except Exception as exc:
                logger.error(msg="Structure of YAML file is incorrect: {}".format(exc))
                raise exc

        # return sanitized path
        return yaml_path

    def check_yaml_buffer(self, yaml_buffer: BufferedIOBase) -> BufferedIOBase:
        """Perform some checks on passed yaml file.

        :param yaml_buffer: bytes reader of the yaml file to check

        :returns: checked bytes object
        :rtype: BufferedIOBase
        """
        # check integrity
        try:
            yaml.safe_load_all(yaml_buffer)
        except yaml.YAMLError as exc:
            logger.error("Invalid YAML {}. Trace: {}".format(yaml_buffer, exc))
            raise exc

        # return sanitized path
        return yaml_buffer

    def validate_scenario(self) -> bool:
        """Validate scenario file.

        :returns: True if scenario is valid, False otherwise
        :rtype: bool
        """
        raise NotImplementedError


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    from pprint import pprint

    reader = ScenarioReader(
        Path("tests/fixtures/scenarios/good_scenario_sample.qdt.yml")
    )
    pprint(reader.yaml_data)
