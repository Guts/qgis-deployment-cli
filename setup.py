#! python3  # noqa: E265

from setuptools import find_packages, setup

# package (to get version)
from qgis_deployment_toolbelt import __about__

setup(
    name="qgis_deployment_toolbelt",
    version=__about__.__version__,
    author=__about__.__author__,
    author_email=__about__.__email__,
    description=__about__.__summary__,
    py_modules=["qgis_deployment_toolbelt"],
    # packaging
    packages=find_packages(
        exclude=["contrib", "docs", "*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    include_package_data=True,
    install_requires=[
        "click>=8,<9",
        "dulwich>=0.20.0,<0.21.0",
        "giturlparse>=0.10,<0.11",
        "pyyaml>=5.4,<7",
        "py-setenv>=1.1,<1.2",
        "send2trash>=1.7.1",
    ],
    entry_points="""
        [console_scripts]
        qdeploy-toolbelt=qgis_deployment_toolbelt.cli:qgis_deployment_toolbelt
        qgis-deployment-toolbelt=qgis_deployment_toolbelt.cli:qgis_deployment_toolbelt
    """,
)
