from pkgutil import iter_modules
from importlib import import_module

for (_, module_name, _) in iter_modules(["qgis_deployment_toolbelt/jobs"]):
    if not module_name.startswith("job_"):
        continue
    print(module_name)
    module = import_module(name=module_name, package="qgis_deployment_toolbelt.jobs")

