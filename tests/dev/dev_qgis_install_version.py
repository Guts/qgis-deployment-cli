import logging

from qgis_deployment_toolbelt.jobs.job_qgis_installation_finder import (
    JobQgisInstallationFinder,
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s||%(levelname)s||%(module)s||%(lineno)d||%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

job = JobQgisInstallationFinder({"version_priority": ["3.36"]})

qgis = job.get_installed_qgis_path()
print(qgis)

print(
    JobQgisInstallationFinder._get_qgis_bin_version(
        "C:\\Program Files\\QGIS 3.34.5\\bin\\qgis-ltr-bin.exe"
    )
)
