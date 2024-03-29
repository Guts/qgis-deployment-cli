# Configuration

## Using environment variables

### CLI arguments

Some options and arguments can be set with environment variables.

| Variable name                       | Corresponding CLI argument | Default value      |
| :---------------------------------- | :------------------------: | :----------------: |
| `QDT_LOGS_LEVEL`                    | `-v`, `--verbose` | `1` (= `logging.WARNING`). Must be an integer. |
| `QDT_PROXY_HTTP`                    | `--proxy-http` to customize network proxy to use. See also [How to use behind a proxy](../guides/howto_behind_proxy.md). | No proxy. |
| `QDT_SCENARIO_PATH`                 | `--scenario` in `deploy`   | `scenario.qdt.yml` |
| `QDT_UPGRADE_CHECK_ONLY`            | `-c`, `--check-only` in `upgrade`   | `False` |
| `QDT_UPGRADE_DISPLAY_RELEASE_NOTES` | `-n`, `--dont-show-release-notes` in `upgrade`   | `True` |
| `QDT_UPGRADE_DOWNLOAD_FOLDER`       | `-w`, `--where` in `upgrade`   | `./` (current folder) |

### Others

Some others parameters can be set using environment variables.

| Variable name       | Description            | Default value      |
| :------------------ | :----------------------: | :----------------: |
| `QDT_LOCAL_WORK_DIR` | Local folder where QDT download remote resources (profiles, plugins, etc.) | `~/.cache/qgis-deployment-toolbelt/default/` |
| `QDT_LOGS_DIR` | Folder where QDT writes the log files, which are automatically rotated. | `~/.cache/qgis-deployment-toolbelt/logs/` |
| `QDT_QGIS_EXE_PATH` | Path to the QGIS executable to use. Used in shortcuts. | `/usr/bin/qgis` on Linux and MacOS, `%PROGRAMFILES%/QGIS 3.28/bin/qgis-ltr-bin.exe` on Windows. |
| `QDT_SSL_USE_SYSTEM_STORES` | By default, a bundle of SSL certificates is used, through [certifi](https://pypi.org/project/certifi/). If this environment variable is set to True, QDT tries to uses the system certificates store. Based on [truststore](https://truststore.readthedocs.io/). See also [How to use custom SSL certificates](../guides/howto_use_custom_ssl_certs.md).  | `False` |
| `QDT_OSGEO4W_INSTALL_DIR` | Path to the OSGEO4W install directory. Used to search for installed QGIS and shortcuts creation. | `C:\\OSGeo4W`. |

----

## 3rd party environment variables

Some of the 3rd party environment variable applies to QDT:

| Variable name       | Description            |
| :------------------ | :----------------------: |
| `REQUESTS_CA_BUNDLE` | Set the path to the bundle of SSL certificates to use for HTTPS requests. See also [How to use custom SSL certificates](../guides/howto_use_custom_ssl_certs.md).  |
| `QGIS_CUSTOM_CONFIG_PATH` | Used to customize the path to the folder where QGIS stores the user's profiles. See [upstream documentation](https://docs.qgis.org/3.34/en/docs/user_manual/introduction/qgis_configuration.html#profiles-path). |
