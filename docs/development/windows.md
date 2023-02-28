# Develop on Windows

Tested on:

- Windows 10 Professional - build 19041 (= version 2004)

## Requirements

- [Python 3.10+ installed with the Windows MSI installer](https://www.python.org/downloads/windows/) (version from the Windows store is not working)
- [Git](https://git-scm.com/download/win) and/or [GitHub Desktop](https://desktop.github.com/)

## Enable remote scripts (for virtual environment)

Open a Powershell prompt as **administrator** inside the repository folder:

```powershell
# if not already done, enable scripts  - required by virtualenv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Installation steps

### Clone the repository

Clone the repository where you want using [GitHub Desktop](https://docs.github.com/en/desktop/installing-and-configuring-github-desktop/installing-and-authenticating-to-github-desktop/setting-up-github-desktop) as graphical interface or a PowerShell terminal:

```powershell
git clone https://github.com/Guts/qgis-deployment-cli.git
# or using ssh
git clone git@github.com:Guts/qgis-deployment-cli.git
```

### Set up the virtual environment

```powershell
# create a virtual env
py -3.10 -m venv .venv

# enable virtual env
.\.venv\Scripts\activate

# upgrade basic tooling
python -m pip install -U pip setuptools wheel

# install dependencies
python -m pip install -U -r requirements/development.txt

# finally, install the package in editable mode
python -m pip install -e .
```

Happy coding!
