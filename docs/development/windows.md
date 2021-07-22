# Develop on Windows

Tested on:

- Windows 10 Professional - build 19041 (= version 2004)

## Requirements

- Python 3.8+ installed with the Windows MSI installer (version from the Windows store is not working)

## Enable remote scripts (for virtual environment)

Open a Powershell prompt as **administrator** inside the repository folder:

```powershell
# if not already done, enable scripts  - required by virtualenv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Installation steps

```powershell
# create a virtual env
py -3.8 -m venv .venv

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
