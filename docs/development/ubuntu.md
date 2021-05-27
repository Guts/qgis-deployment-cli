# Develop on Ubuntu

Tested on:

- Ubuntu 20.04

## Install GDAL

Set GDAL expected version:

```bash
export GDAL_VERSION=3.1.3
```

Install GDAL:

```bash
sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable && sudo apt-get update
sudo apt-get install gdal-bin=$GDAL_VERSION
sudo apt-get install libgdal-dev=$GDAL_VERSION
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
gdal-config --version
```

## Install Python and Git

Install system requirements:

```bash
sudo apt install git python3-pip python3-tk python3-virtualenv python3-venv virtualenv
```

Clone the repository where you want:

```bash
git clone https://github.com/Guts/qgis_deployment_toolbelt.git
# or using ssh
git clone git@github.com:Guts/qgis_deployment_toolbelt.git
```

Create and enter virtual environment (change the path at your convenience):

```bash
virtualenv -p /usr/bin/python3 ~/pyvenvs/qgis_deployment_toolbelt
source ~/pyvenvs/qgis_deployment_toolbelt/bin/activate
```

## Install project requirements

```bash
python -m pip install -U pip setuptools wheel
python -m pip install -U -r requirements/base.txt
python -m pip install pygdal=="`gdal-config --version`.*"
```

```eval_rst
.. note::
    If you want to work outsite a virtual environment, you should install GDAL Python bindings using:

        python -m pip install GDAL=="`gdal-config --version`.*"
```

## Install project

```bash
python -m pip install -e .
```

Try it with:

```bash
python qgis_deployment_toolbelt/qgis_deployment_toolbelt.py
```

Happy coding!
