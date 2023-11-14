# Release workflow

1. Fill the `CHANGELOG.md`
1. Change the version number in `__about__.py`
1. Commit changes with a message like `Bump version to X.x.x` to the main branch
1. Apply a git tag with the relevant version: `git tag -a 0.3.0 {git commit hash} -m "New awesome feature"`
1. Push commit and tag to main branch: `git push --tags`

## Manual upload to PyPi

> This method requires an API token on PyPi

If the CI/CD fails for any reason, here comes the manual procedure:

1. Install required packages:

    ```sh
    python -m pip install -U build twine wheel
    ```

1. Install package in editable mode:

    ```sh
    python -m pip install -e .
    ```

1. Clean previous builds and build package artifacts:

    ```sh
    rm -rf dist/
    python -m build --no-isolation --sdist --wheel --outdir dist/ .
    ```

1. Upload built artifacts to PyPi:

    ```sh
    twine upload -u __token__ dist/*
    ```
