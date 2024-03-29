# Installation

## As a stand-alone executable

1. Download the latest release from [GitHub Release](https://github.com/Guts/qgis-deployment-cli/releases/latest):

  ```{include} download_section.md
  ```

1. Make sure that it's executable (typically on Linux: `chmod u+x ./QGISDeploymentToolbelt_XXXXXX`)
1. Elaborate your scenario (or [grab the sample from the repository](https://github.com/Guts/qgis-deployment-cli/blob/main/scenario.qdt.yml))
1. Run it:
    - from your favorite shell if you like the CLI - see [the relevant section](./cli.md)
    - store your scenario as `scenario.qdt.yml` in the same folder and double-click on the executable

:::{warning}
MacOS version is not tested and is just here to encourage beta-testing and feedback to improve it.
:::

----

## As a Python package

The package is installable with pip:

```sh
pip install qgis-deployment-toolbelt
```

It's then available as a CLI: see [the relevant section](./cli.md)

----

## Using Docker

The package is published as container on GitHub Container Registry (GHCR):

```sh
docker pull ghcr.io/guts/qgis-deployment-cli
```

See [container page for additional options and instructions](https://github.com/Guts/qgis-deployment-cli/pkgs/container/qgis-deployment-cli).
