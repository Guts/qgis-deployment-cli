#! python3  # noqa: E265

"""Setup script to package into a Python module."""

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
from pathlib import Path

# 3rd party
from setuptools import find_packages, setup

# package (to get version)
from qgis_deployment_toolbelt import __about__

# ############################################################################
# ########### Globals ##############
# ##################################

# The directory containing this file
HERE = Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# ############################################################################
# ########### Main #################
# ##################################

setup(
    name=__about__.__package_name__,
    author=__about__.__author__,
    author_email=__about__.__email__,
    description=__about__.__summary__,
    long_description=README,
    long_description_content_type="text/markdown",
    keywords=__about__.__keywords__,
    url=__about__.__uri__,
    version=__about__.__version__,
    classifiers=[
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    # packaging
    py_modules=["qgis_deployment_toolbelt"],
    packages=find_packages(
        exclude=["contrib", "docs", "*.tests", "*.tests.*", "tests.*", "tests", ".venv"]
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
