# Develop on Ubuntu

Tested on:

- Ubuntu 20.04

## Install Python and Git

Install system requirements:

```bash
sudo apt install git python3-pip python3-virtualenv python3-venv virtualenv
```

Clone the repository where you want:

```bash
git clone https://github.com/Guts/qgis-deployment-cli.git
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
python -m pip install -U -r requirements/development.txt
```

## Install project

```bash
python -m pip install -e .
```

Try it with:

```bash
qgis-deployment-toolbelt
```

Happy coding!
