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
from functools import lru_cache
from io import BufferedIOBase
from pathlib import Path
from typing import List, Tuple, Union

# 3rd party
import yaml

# package
from qgis_deployment_toolbelt.utils.check_path import check_path

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

    scenario: dict = None

    def __init__(self, in_yaml: Union[str, Path, BufferedIOBase]):
        """Instanciating YAML scenario reader."""
        # check and get YAML path
        if isinstance(in_yaml, (str, Path)):
            self.input_yaml = self.check_yaml_file(in_yaml)
            # extract data from input file
            with self.input_yaml.open(mode="r") as bytes_data:
                self.scenario = yaml.safe_load(bytes_data)
        elif isinstance(in_yaml, BufferedIOBase):
            self.input_yaml = self.check_yaml_buffer(in_yaml)
            # extract data from input file
            self.scenario = yaml.safe_load(self.input_yaml)
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
        check_path(
            input_path=yaml_path,
            must_be_a_file=True,
            must_exists=True,
            must_be_readable=True,
        )
        yaml_path = Path(yaml_path)

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

    @lru_cache
    def validate_scenario(self) -> Tuple[bool, List[str]]:
        """Validate scenario file.

        TODO: use json schema to validate scenario file.

        :returns: True if scenario is valid, False otherwise and a report of validation
        errors (which is None if the scenario is valid).
        :rtype: Tuple[bool, List[str]]
        """
        # variables
        required_root_keys: tuple = ("metadata", "settings", "steps")

        # outputs
        valid: bool = True
        report: List[str] = []

        # check if scenario is a dict
        if not isinstance(self.scenario, dict):
            report.append(f"Scenario is not a dict but {type(self.scenario)}")
            valid = False

        # check scenario basic structure
        if any([i not in self.scenario for i in required_root_keys]):
            report.append(
                "Some of required root keys are missing: {}".format(
                    ", ".join(required_root_keys)
                )
            )
            valid = False

        # check if metadata is a dict
        if not isinstance(self.metadata, dict):
            report.append("Metadata is not a dict: {}".format(self.metadata))
            valid = False

        return valid, report

    @property
    def metadata(self) -> dict:
        """Get metadata from scenario.

        :returns: metadata
        :rtype: dict
        """
        return self.scenario.get("metadata")

    @property
    def settings(self) -> dict:
        """Get toolbelt settings from scenario.

        :returns: settings
        :rtype: dict
        """
        return self.scenario.get("settings")

    @property
    def steps(self) -> List[dict]:
        """Get steps from scenario.

        :returns: steps
        :rtype: List[dict]
        """
        return self.scenario.get("steps")


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    from pprint import pprint

    reader = ScenarioReader(
        Path("tests/fixtures/scenarios/good_scenario_sample.qdt.yml")
    )
    pprint(reader.scenario)
