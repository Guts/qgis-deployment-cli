# How to use

## As a CLI

To use as a CLI, make sure to remove any `scenario.qdt.yml` file from the current directory.

Then, you can use the following commands:

```sh
qgis-deployment-toolbelt --help
qdeploy-toolbelt --verbose upgrade --check-only
qdt deploy -vv -s https://gitlab.com/Oslandia/qgis/profils_qgis_fr_2022/-/raw/main/qdt_scenarii/scenario.qdt.yml?inline=false
```

See: [Command-line interface usage](./cli.md)

## Sample

```sh
qgis-deployment-toolbelt --help
qdeploy-toolbelt --verbose upgrade --check-only
qdt deploy -vv -s https://gitlab.com/Oslandia/qgis/profils_qgis_fr_2022/-/raw/main/qdt_scenarii/scenario.qdt.yml?inline=false
```

See: [Command-line interface usage](./cli.md)
