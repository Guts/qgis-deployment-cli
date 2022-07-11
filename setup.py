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

with open(HERE / "requirements/base.txt") as f:
    requirements = f.read().splitlines()

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
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: System :: Installation/Setup",
    ],
    # packaging
    py_modules=["qgis_deployment_toolbelt"],
    packages=find_packages(
        exclude=["contrib", "docs", "*.tests", "*.tests.*", "tests.*", "tests", ".venv"]
    ),
    include_package_data=True,
    install_requires=requirements,
    entry_points="""
        [console_scripts]
        qdeploy-toolbelt=qgis_deployment_toolbelt.cli:qgis_deployment_toolbelt
        qgis-deployment-toolbelt=qgis_deployment_toolbelt.cli:qgis_deployment_toolbelt
    """,
)
