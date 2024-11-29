import json
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from qgis_deployment_toolbelt.__about__ import __title_clean__, __version__
from qgis_deployment_toolbelt.utils.file_downloader import download_remote_file_to_local

logging.basicConfig(level=logging.WARNING)

base_url = "https://raw.githubusercontent.com/qgis-deployment/qgis-deployment-toolbelt-cli/main/examples/"
target_folder = Path(__file__).parent.joinpath(
    "../fixtures/tmp/test-http-batch-downloader"
)
test_qdt_files = Path(__file__).parent.joinpath(
    "../fixtures/http-test-local/qdt-files.json"
)
if not test_qdt_files.exists():
    download_remote_file_to_local(
        remote_url_to_download=f"{base_url}qdt-files.json",
        local_file_path=test_qdt_files,
    )


def tree_to_download_list(tree_array: list[dict], rel_path: str = "") -> list:
    li_files = []

    for item in tree_array:
        print(item)
        if item.get("type") == "directory":
            if item.get("name") != ".":
                new_rel_path = f"{rel_path}/{item.get('name')}"
            else:
                new_rel_path = f"{item.get('name')}"
            li_files.extend(
                tree_to_download_list(
                    tree_array=item.get("contents"),
                    rel_path=new_rel_path,
                )
            )
        elif item.get("type") == "file":
            li_files.append(f"{rel_path}/{item.get('name')}")

    return li_files


with test_qdt_files.open(mode="r", encoding="utf-8") as in_json:
    qdt_tree = json.load(in_json)


# print(qdt_tree[0].keys())
# print(len(qdt_tree))

# check report
for child in qdt_tree:
    if child.get("type") == "report":
        logging.info(
            f"Listed: {child.get('files')} files in {child.get('directories')} folders"
        )
        break

# check folders
li_files_to_download = tree_to_download_list(tree_array=qdt_tree)


# print(li_files_to_download)

li_succeeded_downloads: list[tuple[str, Path]] = []
li_failed_downloads: list[tuple[str, str]] = []

with ThreadPoolExecutor(
    thread_name_prefix=f"{__title_clean__}_profile_sync"
) as executor:
    for fifi in li_files_to_download:
        # submit download to pool
        try:
            executor.submit(
                # func to execute
                download_remote_file_to_local,
                # func parameters
                local_file_path=target_folder.joinpath(fifi),
                remote_url_to_download=f"{base_url}{fifi}",
            )
            li_succeeded_downloads.append(
                (f"{base_url}{fifi}", target_folder.joinpath(fifi))
            )
        except Exception as err:
            li_failed_downloads.append((fifi, f"{err}"))

# for fifi in li_files_to_download:
#     try:
#         download_remote_file_to_local(
#             remote_url_to_download=f"{base_url}{fifi}",
#             local_file_path=target_folder.joinpath(fifi),
#         )
#     except Exception as err:
#         li_failed_downloads.append((fifi, f"{err}"))


if len(li_failed_downloads):
    logging.warning("Some files have not been downloaded: ")
    for i in li_failed_downloads:
        print(i)
