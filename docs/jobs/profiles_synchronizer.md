# Profiles Synchronizer

This job synchronizes installed profiles (those stored in QGIS profiles folder) from the downloaded ones (those stored in QDT local folder).

----

## Use it

Sample job configurations.

### Update or install profiles only with a newer version number

```yaml
- name: Synchronize installed profiles from downloaded ones
  uses: qprofiles-synchronizer
  with:
    sync_mode: only_new_version
```

### Systematically overwrite installed profile with downloaded one

```yaml
- name: Synchronize installed profiles from downloaded ones
  uses: qprofiles-synchronizer
  with:
    sync_mode: overwrite
```

----

## Vocabulary

### Profiles states

- `remote`: a profile stored outside the end-user computer, on a git repository, an HTTP server or a LAN drive. Typically: `https://gitlab.com/Oslandia/qgis/profils_qgis_fr.git`.
- `downloaded`: a profile downloaded into the QDT local working folder. Typically: `~/.cache/qgis-deployment-toolbelt/Oslandia/`.
- `installed`: a profile's folder located into the QGIS profiles folder and so accessible to the end-user through the QGIS interface. Typically: `~/.local/share/QGIS/QGIS3/profiles/default` or `%APPDATA%/QGIS/QGIS3/profiles/default`

----

## Options

### sync_mode

Synchronization mode to apply with profiles.

Possible_values:

- `only_missing` (_default_): only install profiles that does not exist locally
- `only_different_version`: only install profiles that does not exist locally and update those with a different version number (lesser or upper)
- `only_new_version`: only install profiles that does not exist locally and update those with a lesser version number
- `overwrite`: systematically overwrite local profiles
