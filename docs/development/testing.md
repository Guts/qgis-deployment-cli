# Tests

The project aims to be fully tested on every targetted platform through intensive CI/CD on every Pull Request.

Still, it's preferable to run tests locally before pushing to the public remote repository.

## Structure

- tests are located in the `tests` subfolder
- a test file is prefixed with `test_`
- ideally a test is written using the standard library, so as a "pure" unittest class, even if for some needs the pytest framework can be used.
- quick tests scripts can be stored in `tests/dev` folder to illustrate or check a behavior

## Requirements

To run the tests, you need to install development requirements ([Ubuntu](./ubuntu.md#develop-on-ubuntu) or [Windows](./windows.md#develop-on-windows)).

Complete it by installing tests requirements:

```sh
python -m pip install -U -r requirements/testing.txt
```

## Run

Simply run Pytest:

```sh
pytest
```

It's also possible to run an individual test:

```sh
python -m unittest tests.test_qplugin_object.TestQgisPluginObject.test_profile_load_from_json_basic
```
