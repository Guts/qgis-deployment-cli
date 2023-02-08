#! python3  # noqa: E265

"""
    Sub-command in charge of checking if new versions are available.

    Author: Julien M. (https://github.com/guts)
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import json
import logging
from pathlib import Path
from sys import platform as opersys
from urllib.parse import urlsplit, urlunsplit
from urllib.request import urlopen

# 3rd party library
import click
from packaging.version import Version
from rich.console import Console
from rich.markdown import Markdown

# submodules
from qgis_deployment_toolbelt.__about__ import __title__, __uri_repository__
from qgis_deployment_toolbelt.__about__ import __version__ as actual_version
from qgis_deployment_toolbelt.utils.bouncer import (
    exit_cli_error,
    exit_cli_normal,
    exit_cli_success,
)
from qgis_deployment_toolbelt.utils.file_downloader import download_remote_file_to_local

# #############################################################################
# ########## Globals ###############
# ##################################

# logs
logger = logging.getLogger(__name__)


# #############################################################################
# ####### Functions ###############
# #################################


def get_download_url_for_os(release_assets: list) -> str:
    """Parse list of a GitHub release assets and return the appropriate download URL \
        for the current operating system.

    Args:
        release_assets (list): list of assets

    Returns:
        str: asset download URL (browser_download_url)
    """
    for asset in release_assets:
        if opersys == "win32" and "Windows" in asset.get("name"):
            return asset.get("browser_download_url"), asset.get("content-type")
        elif opersys == "linux" and "Ubuntu" in asset.get("name"):
            return asset.get("browser_download_url"), asset.get("content-type")
        elif opersys == "darwin" and "MacOS" in asset.get("name"):
            return asset.get("browser_download_url"), asset.get("content-type")
        else:
            continue

    return None


def get_latest_release(api_repo_url: str) -> dict:
    """Get latest release from GitHub public API.

    Args:
        api_repo_url (str): API URL with the owner and repository set

    Returns:
        dict: GitHub release object
    """

    request_url = f"{api_repo_url}releases/latest"
    try:
        response = urlopen(request_url)
        if response.status == 200:
            release_info = json.loads(response.read())
            return release_info
    except Exception as err:
        logger.error(err)
        return None


def replace_domain(url: str, new_domain: str) -> str:
    """
    Replaces the domain of an URL with a new domain.

    Args:
        url (str): The original URL.
        new_domain (str): The new domain to replace the original domain with.

    Returns:
        str: The URL with the new domain.
    """
    split_url = urlsplit(url)
    split_url = split_url._replace(netloc=new_domain)
    new_url = urlunsplit(split_url)
    return new_url


# #############################################################################
# ####### Command-line ############
# #################################
@click.command()
@click.option(
    "-c",
    "--check-only",
    help="Only check if a new version is available. No download.",
    is_flag=True,
    show_default=True,
)
@click.option(
    "-w",
    "--where",
    help="Folder to store the downloaded file.",
    default="./",
    show_default=True,
    type=click.Path(file_okay=False, dir_okay=True, writable=True, resolve_path=True),
)
def upgrade(check_only: bool, where: Path):
    """Check if a newer version of the cli is available."""
    console = Console()
    # build API URL from repository
    api_url = replace_domain(url=__uri_repository__, new_domain="api.github.com/repos")

    # get latest release as dictionary
    latest_release = get_latest_release(api_repo_url=api_url)

    if not latest_release:
        exit_cli_error(f"Unable to retrieve latest release from {api_url}.")

    # compare it
    latest_version = latest_release.get("tag_name")
    if Version(actual_version) < Version(latest_version):
        console.print(f"A newer version is available: {latest_version}")
        version_change = Markdown(latest_release.get("body"))
        console.print(version_change)
        if check_only:
            exit_cli_normal(
                f"A newer version is available: {latest_version}", abort=True
            )
        else:
            exit_cli_normal(
                f"A newer version is available: {latest_version}",
                abort=False,
            )
    else:
        exit_cli_success(f"You are already using the latest version: {latest_version}")

    # -- DOWNLOAD ------------------------------------------------------------

    # select remote download URL
    remote_url, remote_content_type = get_download_url_for_os(
        latest_release.get("assets")
    )
    if not remote_url:
        exit_cli_error(f"Unable to identify an appropriate download URL for {opersys}.")

    # destination local file
    dest_filepath = Path(where, Path(urlsplit(remote_url).path).name)

    # download it
    logger.info(
        f"Downloading new version '{latest_version}' from {remote_url} to {dest_filepath}"
    )
    try:
        download_remote_file_to_local(
            remote_url_to_download=remote_url,
            local_file_path=dest_filepath,
            content_type=remote_content_type,
        )
    except Exception as err:
        exit_cli_error(f"Download new version failed. Trace: {err}")

    exit_cli_success(f"New version of {__title__} downloaded here: {dest_filepath}.")


# #############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """Standalone execution."""
    upgrade(obj={})
