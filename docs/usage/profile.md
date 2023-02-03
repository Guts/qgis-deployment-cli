# Describe and prepare your QGIS profiles

QDT is designed to work with QGIS profiles that allow different configurations (plugins, connections, symbologies, expressions, templates, etc.) to be segmented for different uses on the same installation.

In order to avoid unnecessary duplication of code (typically that of the various plugins) or configuration files and to make deployment reproducible, QDT relies on a profile definition file: `profile.json`.

## Publish them

## Good practices and recomendations

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

----

## Sample profile.json

```{eval-rst}
.. literalinclude:: ../../tests/fixtures/profiles/good_sample_profile.json
  :language: json
```
