# Describe and prepare your QGIS profiles

QDT is designed to work with QGIS profiles that allow different configurations (plugins, connections, symbologies, expressions, templates, etc.) to be segmented for different uses on the same installation.

In order to avoid unnecessary duplication of code (typically that of the various plugins) or configuration files and to make deployment reproducible, QDT relies on a profile definition file: `profile.json`.

QDT expects to find this file in the folder of each profile stored in the source of synchronized profiles in the qprofiles-manager job.

## Publish them

3 options:

- on a remote Git repository (github.com, gitlab.com, GitLab instance...)
- on a local Git repository
- on a web server through HTTP using a `qdt.json`

## Typical structure of a project with profiles

Given 3 profiles to be deployed: `avdanced`, `beginner` and `readonly`. Here comes a typical organization of folders, subfolers and files into your repository:

```sh
qgis-profiles/
├── .git/
├── LICENSE
├── profiles
│   ├── advanced
│   │   ├── images
│   │   │   ├── profile_advanced.ico
│   │   │   └── splash.png
│   │   ├── profile.json
│   │   └── QGIS
│   │       ├── QGIS3.ini
│   ├── beginner
│   │   ├── images
│   │   │   ├── profile_beginner.ico
│   │   │   └── splash.png
│   │   ├── profile.json
│   │   └── QGIS
│   │       ├── QGIS3.ini
│   │       └── QGISCUSTOMIZATION3.ini
│   └── readonly
│       ├── bookmarks.xml
│       ├── images
│       │   └── profile_readonly.ico
│       ├── profile.json
│       ├── project_default.qgs
│       └── QGIS
│           └── QGIS3.ini
│           └── QGISCUSTOMIZATION3.ini
├── qdt
│   └── scenario.qdt.yml
├── README.md
```

----

## Good practices and recomendations

- if you use a Git repository, store profiles in a subfolder not at the project root and specify the relative path in scenario
- do not store the entire profile folder, but only files that contans something specific to your profile
- keep only the lines of `*.ini` files which are custom to your profile:
  - QGIS will fill them automatically if needed
  - it reduces the surface of possible conflicts when dealing to upgrade a profile

----

## Model definition

The project comes with a [JSON schema]("https://raw.githubusercontent.com/Guts/qgis-deployment-cli/main/docs/schemas/profile/qgis_profile.json",) describing the model of a profile:

```{eval-rst}
.. literalinclude:: ../schemas/profile/qgis_profile.json
  :language: json
```

With a submodel for plugin object:

```{eval-rst}
.. literalinclude:: ../schemas/profile/qgis_plugin.json
  :language: json
```

:::{tip}
To retrieve the ID of a plugin see [this page](../misc/tip_get_plugin_id.md).
:::

----

## Sample profile.json

```{eval-rst}
.. literalinclude:: ../../tests/fixtures/profiles/good_sample_profile.json
  :language: json
```
