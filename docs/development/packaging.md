# Packaging

## Packaging into an executable

The project takes advantage of [PyInstaller](https://pyinstaller.readthedocs.io/) to package the application into an executable.

The output binary and all embedded dependencies is located into a subfolder named: `dist/qgis_deployment_toolbelt_{version}_{operating-system}_Python{python-version}`.

### Windows

> Comply with [Windows development requirements](windows) before to run.

```powershell
# Generates MS Version Info
python .\builder\version_info_templater.py

# Generates MS Executable
python -O .\builder\pyinstaller_build_windows.py
```

![QGIS Deployment Toolbelt - Executable properties](/static/executable_windows_properties_details.png)

To run it, double-click on the executable file (*.exe).

### Ubuntu

> Comply with [Ubuntu development requirements](ubuntu) before to run.

```bash
# Generates binary executable
python -O ./builder/pyinstaller_build_ubuntu.py
```

To run it, for example:

```bash
cd dist/qgis_deployment_toolbelt_3-0-0_Ubuntu20-04_64bit_Python3-8-5/
./qgis_deployment_toolbelt_3-0-0_Ubuntu20-04_64bit_Python3-8-5
```

----

## Docker

:::{note}
Image is meant to be used, not to develop. So, it does not contain side code: `docs`, `tests`, etc.  
If you need that, edit the `.dockerignore` file.
:::

### Requirements

- Docker >= 20.10

### Build

```sh
docker build --pull --rm -f "Dockerfile" -t qdt:latest "."
```

### Run within the container

Enter into the container and run commands interactively::

```sh
> docker run --rm -it qdt:latest
root@55c5de0191ee:/user/app# qdt --version
0.23.1
```

Run QDT directly from the container:

```sh
> docker run --rm qdt:latest qdt --version
0.23.1
```
