# Plugins synchronizer

This job synchronize plugins between those stored locally (typically downloaded by the Plugins Downloader job) and the installed plugins.

----

## Use it

Sample job configuration in your scenario file:

```yaml
  - name: Synchronize plugins
    uses: qplugins-synchronizer
    with:
      force: false
```

----

## Options

### action

Tell the job what to do with plugins in **installed profiles**:

Possible_values:

- `create`: add plugins if they are not present
- `create_or_restore`: add plugins if not present and replace eventual existing one
- `remove`: remove plugins which are not listed

### source

Where to find plugins zip files.

Possible_values: a valid path to an existing folder

Default: `~/.cache/qgis-deployment-toolbelt/plugins`

----

## How does it work

### Workflow

1. List plugins archives into the source folder. Default: `~/.cache/qgis-deployment-toolbelt/plugins`
1. Parse profiles installed
1. Compare plugin versions between referenced in profile.json and the one installed
1. If version plugin in installed profile is inferior, unzip the download plugin in installed profiles
