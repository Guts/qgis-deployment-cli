# Profiles manager

This job synchronize local profiles with remote storage (git for now).

----

## Use it

Sample job configurations.

### Public **remote** git repository in **overwrite** mode

```yaml
- name: Synchronize profiles from remote git repository
  uses: qprofiles-manager
  with:
    action: download
    branch: main
    protocol: git
    source: https://github.com/geotribu/profils-qgis.git
    sync_mode: overwrite
```

### **Local** git repository

```yaml
- name: Synchronize profiles from local git repository
  uses: qprofiles-manager
  with:
    action: download
    branch: main
    protocol: git
    source: file:///home/jmo/Git/Geotribu/profils-qgis
    sync_mode: only_new_version
```

----

## Vocabulary

### Profiles states

- `remote`: a profile stored outside the end-user computer, on a git repository, an HTTP server or a LAN drive. Typically: `https://gitlab.com/Oslandia/qgis/profils_qgis_fr_2022.git`.
- `downloaded`: a profile downloaded into the QDT local working folder. Typically: `~/.cache/qgis-deployment-toolbelt/Oslandia/`.
- `installed`: a profile's folder located into the QGIS profiles folder and so accessible to the end-user through the QGIS interface. Typically: `~/.local/share/QGIS/QGIS3/profiles/default` or `%APPDATA%/QGIS/QGIS3/profiles/default`

----

## Options

### branch

Name of the branch to use when working with a git repository.

### protocol

Set which protocol to use.

Possible_values:

- `git` (_default_): use git to clone or pull changes from remote repository. `source` must end with `.git` and `branch` should also be set.
- `http`: use HTTP to download remote profiles. Source must start with `http`.

### source

Location of profiles to use as reference.

Must start with:

- `file://`: for local disk or network
- `git://` (_recomended_): for git repositories
- `https://`: for profiles stored into git repositories accessible through HTTP or profiles downloadable through an HTTP server

### sync_mode

Synchronization mode to apply with profiles.

Possible_values:

- `only_missing` (_default_): only install profiles that does not exist locally
- `only_different_version`: only install profiles that does not exist locally and update those with a different version number (lesser or upper)
- `only_new_version`: only install profiles that does not exist locally and update those with a lesser version number
- `overwrite`: systematically overwrite local profiles
