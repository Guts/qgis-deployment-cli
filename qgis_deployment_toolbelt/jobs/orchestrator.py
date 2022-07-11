#! python3  # noqa: E265

"""
    Read and validate scenario files.

    Author: Julien Moura (https://github.com/guts, Oslandia)
"""


# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import importlib
import logging
from pathlib import Path
from typing import List, Tuple

from qgis_deployment_toolbelt.jobs.job_environment_variables import (
    JobEnvironmentVariables,
)
from qgis_deployment_toolbelt.jobs.job_profiles_synchronizer import (
    JobProfilesDownloader,
)
from qgis_deployment_toolbelt.jobs.job_shortcuts import JobShortcutsManager

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)

# #############################################################################
# ########## Classes ###############
# ##################################


class JobsOrchestrator:
    """Orchestrate jobs."""

    JOBS = (JobEnvironmentVariables, JobProfilesDownloader, JobShortcutsManager)
    PACKAGE_NAME: str = "qgis_deployment_toolbelt.jobs"

    def __init__(self) -> None:
        pass

    @property
    def available_jobs(self) -> List[Path]:
        """List all available jobs."""
        # job modules
        return list(Path(__file__).parent.glob("job_*.py"))

    @property
    def jobs_ids(self) -> Tuple[str]:
        """Returns available jobs ID.

        :return Tuple[str]: jobs ids
        """
        return tuple([job.ID for job in self.JOBS])

    def get_job_module_from_id(self, job_id: str) -> object:
        """Get job class from id.

        :param str job_id: job identifier (as defined in scenario file)
        :return object: Job class
        """
        for job in self.JOBS:
            if job.ID == job_id:
                return job

    def init_job_class_from_id(self, job_id: str, options: dict) -> object:
        """Get job class from id and instanciate it with options.

        :param str job_id: job identifier (i.e. "qprofiles-manager")
        :param dict options: job options

        :return object: instanciated job class with options
        """
        return self.get_job_module_from_id(job_id)(options)

    def import_job(self, job_name: str):
        """Import a job."""
        return importlib.import_module(name=job_name, package=self.PACKAGE_NAME)

    def import_all_jobs(self) -> None:
        """Import all jobs."""
        for module in self.available_jobs:
            self.JOBS[module.stem] = self.import_job(module.stem)


# #############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == "__main__":
    """Standalone execution."""
    pass
