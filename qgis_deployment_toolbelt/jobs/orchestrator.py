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

    JOBS = (JobEnvironmentVariables, JobProfilesDownloader)
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
        """Get job class from id."""
        for job in self.JOBS:
            if job.ID == job_id:
                return job

    def init_job_class_from_id(self, job_id: str, options: dict) -> object:
        """Get job class from id and instanciate it with options."""
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
    import inspect
    from pprint import pprint

    from generic import JobBase

    # mod = importlib.import_module(
    #     name="job_environment_variables", package="qgis_deployment_toolbelt.jobs"
    # )
    # print(mod.__doc__, mod.__name__, dir(mod))

    orchestrator = JobsOrchestrator()
    jobs_available = orchestrator.available_jobs

    j = orchestrator.import_job("job_environment_variables")
    print(j.__doc__, j.__name__, dir(j))

    # orchestrator.import_all_jobs()

    # pprint(orchestrator.JOBS)

    # for k, v in orchestrator.JOBS.items():
    #     print(v, type(v), dir(v))
    #     for name_local in dir(v):
    #         if name_local.startswith("__"):
    #             continue
    #         module_class = getattr(v, name_local)
    #         print(str(module_class), type(module_class))
    # #         print(name_local, isclass(getattr(v, name_local)))
    #         # print(name_local, issubclass(getattr(v, name_local), JobBase))
    #         print(module_class, issubclass(getattr(v, module_class), JobBase))
    # #         print(name_local, isinstance(getattr(v, name_local), JobBase))
    #         if isclass(getattr(v, name_local)) and isinstance(getattr(v, name_local), JobBase):
    #             print("test " + name_local)
    #             # print(f"{k} - {name_local.ID}")
    #         # for name_local in dir(v):
    #         #     if inspect.isclass(getattr(v, name_local)):
    #         #         print(f'{name_local} is a class')
    #         #         MysteriousClass = getattr(v, name_local)
    #         #         mysterious_object = MysteriousClass()

    # READ https://julienharbulot.com/python-dynamical-import.html

    # from inspect import isclass
    # from pkgutil import iter_modules
    # from pathlib import Path
    # from importlib import import_module

    # # iterate through the modules in the current package
    # package_dir = Path(__file__).resolve().parent
    # for (_, module_name, _) in iter_modules([package_dir]):

    #     # import the module and iterate through its attributes
    #     module = import_module(f"{__name__}.{module_name}")
    #     for attribute_name in dir(module):
    #         attribute = getattr(module, attribute_name)

    #         if issubclass(attribute, JobBase):
    #             # Add the class to this package's variables
    #             globals()[attribute_name] = attribute
