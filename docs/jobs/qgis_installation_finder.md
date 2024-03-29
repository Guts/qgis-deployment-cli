# QGIS installation finder

Use this job to find installed QGIS version for automatic definition of QDT environnement variable `QDT_QGIS_EXE_PATH` needed for shortcut creation

----

## Compatibility

This job is compatible with:

- Windows
- Linux

----

## Use it

Sample job configuration in your scenario file:

```yaml
- name: Find installed QGIS
  uses: qgis-installation-finder
  with:
    version_priority:
      - "3.36"
    if_not_found: error
```

----

## Options

### version_priority

Multiple versions of QGIS can be installed on Windows.

This option is used to specify the preferred QGIS version

For example if you define :

```yaml
- name: Find installed QGIS
  uses: qgis-installation-finder
  with:
    version_priority:
      - "3.34"
      - "3.36"
```

QDT will first use 3.34.z versions. If none are available it will use 3.36.z versions.

If multiple 3.34.z versions are available, the latest will be used. For example if 3.34.1 and 3.34.5 version are available, 3.34.5 will be used.

If no version from version_priority` is available, it will use the latest found version.

### if_not_found

This option determines the action to be taken if QGIS is not found during the search process.

Possible_values:

- `warning` (_default_): if no version found, a warning is displayed in QDT logs
- `error`: if no version found, QDT stop and the other jobs are not run

----

## How does it work

On Linux, QDT locate installed QGIS with `which`command.

On Windows QDT try to locate installed versions in the current directories :

- `%PROGRAMFILES%\\QGIS x.y.z\\bin\`
- `%QDT_OSGEO4W_INSTALL_DIR%` (default value : `C:\\OSGeo4W`)

By default, the latest version found is used.

----

## Schema

```{eval-rst}
.. literalinclude:: ../schemas/scenario/jobs/qgis-installation-finder.json
  :language: json
```
