# Configuration

## Using environment variables

### CLI arguments

Some options and arguments can be set with environment variables.

| Variable name       | Corresponding CLI argument | Default value      |
| :------------------ | :------------------------: | :----------------: |
| `QDT_LOGS_LEVEL` | `-v`, `--verbose` | `1` (= `logging.WARNING`). Must be an integer. |
| `QDT_UPGRADE_CHECK_ONLY` | `-c`, `--check-only` in `upgrade`   | `False` |
| `QDT_UPGRADE_DISPLAY_RELEASE_NOTES` | `-n`, `--dont-show-release-notes` in `upgrade`   | `True` |
| `QDT_UPGRADE_DOWNLOAD_FOLDER` | `-w`, `--where` in `upgrade`   | `./` (current folder) |
| `QDT_SCENARIO_PATH` | `--scenario` in `deploy`   | `scenario.qdt.yml` |

### Others

Some others parameters can be set using environment variables.

| Variable name       | Description            | Default value      |
| :------------------ | :----------------------: | :----------------: |
| `QDT_LOCAL_WORK_DIR` | Local folder where QDT download remote resources (profiles, plugins, etc.) | `~/.cache/qgis-deployment-toolbelt/default/` |
| `QDT_LOGS_DIR` | Folder where QDT writes the log files, which are automatically rotated. | `~/.cache/qgis-deployment-toolbelt/logs/` |
