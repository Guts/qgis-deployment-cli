#! python3  # noqa E265

"""Usage from the repo root folder:

.. code-block:: python

    # for whole test
    python -m unittest tests.test_job_profiles_downloader
    # for specific
    python -m unittest tests.test_job_profiles_downloader.TestJobProfilesDownloader.test_run_refreshes_cached_downloaded_profiles
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import json
import tempfile
import unittest
from os import environ
from pathlib import Path
from unittest.mock import patch

# 3rd party
from git import Repo as GitPythonRepo

# package
from qgis_deployment_toolbelt.jobs.generic_job import GenericJob
from qgis_deployment_toolbelt.jobs.job_profiles_downloader import (
    JobProfilesDownloader,
)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestJobProfilesDownloader(unittest.TestCase):
    """Test profiles downloader job."""

    # -- Helpers -----------------------------------------------------------------
    @staticmethod
    def _commit_profile(
        repo: GitPythonRepo, name: str, version: str | None, message: str
    ) -> None:
        """Write (or remove if version is None) a profile and commit it."""
        profile_folder = Path(repo.working_dir, name)
        if version is None:
            repo.index.remove([str(profile_folder / "profile.json")], working_tree=True)
        else:
            profile_folder.mkdir(exist_ok=True)
            profile_folder.joinpath("profile.json").write_text(
                json.dumps({"name": name, "version": version}), encoding="UTF-8"
            )
            repo.index.add([str(profile_folder / "profile.json")])
        repo.index.commit(message)

    def _run_downloader(self, source: Path) -> JobProfilesDownloader:
        """Run the job against a local git repository."""
        job = JobProfilesDownloader(
            options={
                "branch": "main",
                "protocol": "git_local",
                "source": source.resolve().as_uri(),
            }
        )
        job.run()
        return job

    # -- Tests -------------------------------------------------------------------
    def test_run_refreshes_cached_downloaded_profiles(self):
        """Profiles listed by a previous job (e.g. cleanup-manager placed first)
        must not hide the freshly downloaded ones: an updated profile must be seen
        with its new version, a profile removed upstream must not be listed."""
        cases = {
            "version updated": (("demo", "2.0.0"), ("legacy", "1.0.0")),
            "profile removed": (("demo", "2.0.0"), ("legacy", None)),
        }
        for label, upstream_changes in cases.items():
            with (
                self.subTest(case=label),
                tempfile.TemporaryDirectory(prefix="QDT_test_profiles_dl_") as tmp_dir,
                patch.dict(environ, {"QDT_LOCAL_WORK_DIR": f"{tmp_dir}/qdt_work"}),
                patch.dict(GenericJob.PROFILES_FOLDER_CACHE, clear=True),
                patch.dict(GenericJob.RULES_FILTER_CACHE, clear=True),
                # closed before the temporary folder removal: GitPython keeps
                # 'git cat-file' processes running in the repository folder, which
                # prevents its deletion on Windows (WinError 32)
                GitPythonRepo.init(
                    Path(tmp_dir, "remote"), initial_branch="main"
                ) as repo,
            ):
                source = Path(repo.working_dir)
                self._commit_profile(repo, "demo", "1.0.0", "add demo")
                self._commit_profile(repo, "legacy", "1.0.0", "add legacy")

                # previous run: profiles already downloaded and listed
                job = self._run_downloader(source)
                self.assertEqual(
                    sorted((p.name, p.version) for p in job.list_downloaded_profiles()),
                    [("demo", "1.0.0"), ("legacy", "1.0.0")],
                )

                for name, version in upstream_changes:
                    if version != "1.0.0":
                        self._commit_profile(repo, name, version, f"change {name}")

                job = self._run_downloader(source)
                expected = sorted(
                    (name, version)
                    for name, version in upstream_changes
                    if version is not None
                )
                self.assertEqual(
                    sorted((p.name, p.version) for p in job.list_downloaded_profiles()),
                    expected,
                )
                self.assertEqual(
                    sorted(job.PROFILES_NAMES_DOWNLOADED), [n for n, _ in expected]
                )


# ############################################################################
# ####### Stand-alone run ########
# ################################
if __name__ == "__main__":
    unittest.main()
