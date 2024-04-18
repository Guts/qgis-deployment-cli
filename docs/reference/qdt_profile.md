# QDT Profile

## Rules

You can add rules to make the profile deployment conditional. In the following example, the profile will be deployed only on Linux:

```json
{
  "$schema": "https://raw.githubusercontent.com/Guts/qgis-deployment-cli/main/docs/schemas/profile/qgis_profile.json",
  "name": "only_linux",
  "folder_name": "qdt_only_linux",
  "description": "A QGIS profile for QDT with a conditional deployment rule.",
  "author": "Julien Moura",
  "email": "infos+qdt@oslandia.com",
  "qgisMinimumVersion": "3.34.0",
  "qgisMaximumVersion": "3.99.10",
  "version": "1.7.0",
  "rules": [
    {
      "name": "Environment",
      "description": "Profile is configured to run only on Linux.",
      "conditions": {
        "all": [
          {
            "path": "$.environment.operating_system_code",
            "value": "linux",
            "operator": "equal"
          }
        ]
      }
    }
  ]
}
```

## Model definition

The project comes with a [JSON schema](https://raw.githubusercontent.com/Guts/qgis-deployment-cli/main/docs/schemas/profile/qgis_profile.json) describing the model of a profile:

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
To retrieve the ID of a plugin see [this page](../guides/howto_qgis_get_plugin_id.md).
:::

----

## Sample profile.json

```{eval-rst}
.. literalinclude:: ../../tests/fixtures/profiles/good_sample_profile.json
  :language: json
```
