# Command-line interface usage

## Main command

```{sphinx_argparse_cli}
  :module: qgis_deployment_toolbelt.cli
  :hook:
  :func: main
  :prog: qgis-deployment-toolbelt
  :title: Commands and options
```

----

## Environment variables

Some options and arguments can be set with environment variables.

| Variable name       | Corresponding CLI argument | Default value      |
| :------------------ | :------------------------: | :----------------: |
| `QDT_UPGRADE_CHECK_ONLY` | `-c`, `--check-only` in `upgrade`   | `False` |
| `QDT_UPGRADE_DISPLAY_RELEASE_NOTES` | `-n`, `--dont-show-release-notes` in `upgrade`   | `True` |
| `QDT_UPGRADE_DOWNLOAD_FOLDER` | `-w`, `--where` in `upgrade`   | `./` (current folder) |
| `QDT_SCENARIO_PATH` | `--scenario` in `deploy`   | `scenario.qdt.yml` |
