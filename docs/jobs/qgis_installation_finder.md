# QGIS installation finder

Use this job to find installed QGIS version to auto definition QDT environnement variable `QDT_QGIS_EXE_PATH` needed for shortcut creation

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

Multiple QGIS version can be installed in Windows, this option prioritize the version to use.

It define a list of version to use by priority.

### if_not_found

Job behavior if QGIS is not found.

Possible_values:

- `warning` (_default_): if no version found, a warning is displayed in QDT logs
- `error`: if no version found, QDT stop and the other jobs are not run

----

## How does it work

On Linux, QDT locate installed QGIS with `which`command.

On Windows QDT try to locate installed versions in the current directories :

- `%PROGRAMFILES%\\QGIS x.y.z\\bin\`
- `%QDT_OSGEO4W_INSTALL_DIR%` (default value : `C:\\OSGeo4W`)

By default, the latest version is used.

----

## Schema

```{eval-rst}
.. literalinclude:: ../schemas/scenario/jobs/qgis-installation-finder.json
  :language: json
```
