from pathlib import Path

from qgis_deployment_toolbelt.utils.file_downloader import download_remote_file_to_local

# Should not use proxy
remote_url_to_download: str = (
    "https://sigweb-rec.grandlyon.fr/qgis/plugins/dtdict.0.1.zip"
    
)

local_file_path: Path = Path("tests/fixtures/tmp/").joinpath(
    remote_url_to_download.split("/")[-1]
)
local_file_path.parent.mkdir(parents=True, exist_ok=True)

# Should use proxy
remote_url_to_download: str = (
    "https://plugins.qgis.org/plugins/french_locator_filter/version/1.1.1/download/"    
)

local_file_path: Path = Path("tests/fixtures/tmp/french_locator_filter.zip")
local_file_path.parent.mkdir(parents=True, exist_ok=True)


download_remote_file_to_local(remote_url_to_download=remote_url_to_download,
                              local_file_path=local_file_path)
