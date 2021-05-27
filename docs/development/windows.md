# Develop on Windows

Tested on:

- Windows 10 Professional - build 19041 (= version 2004)

## Common

### Enable remote scripts (for virtual environment)

Open a Powershell prompt as **administrator** inside the repository folder:

```powershell
# if not already done, enable scripts  - required by virtualenv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

----

## Using pre-built wheel

### Requirements

- Python 3.7+ installed with the Windows MSI installer (version from the Windows store is not working)

### Download GDAL wheel

1. Go to <https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal>
2. Download the adequate package. For example: `GDAL‑3.1.3‑cp37‑cp37m‑win_amd64.whl`
3. Move downloaded wheel to the `lib` subfolder

### Installation steps

```powershell
# create a virtual env
py -3.7 -m venv .venv

# enable virtual env
.\.venv\Scripts\activate

# upgrade basic tooling
python -m pip install -U pip

# install dependencies
python -m pip install -U -r requirements/base.txt
python -m pip install -U -r requirements/development.txt

# finally, install the package in editable mode
python -m pip install -e .
```

Happy coding!
