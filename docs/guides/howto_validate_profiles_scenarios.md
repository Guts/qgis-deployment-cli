# How to automatically validate QDT files

In order to minimize friction and maximize productivity, the project provides a [schema.json](https://json-schema.org/) for scenarios and profiles files.

## Text editors (IDE)

If your editor supports JSON and YAML schema validation, it's definitely recommended to set it up. Here is a demonstration on how it works in Visual Studio Code:

<!-- markdownlint-disable MD033 -->
<video preload="metadata" width="100%" controls>
  <source src="../_static/qdt_assisted_edition_vscode.webm" type="video/webm">
  Your browser does not support HTML 5 video tag.
</video>
<!-- markdownlint-enable MD033 -->

### Visual Studio Code

#### Profiles

Add the following line at the top of your JSON file:

```json
{
  "$schema": "https://raw.githubusercontent.com/qgis-deployment/qgis-deployment-toolbelt-cli/main/docs/schemas/profile/qgis_profile.json"
  [...]
}
```

#### Scenarios

1. Install the [vscode-yaml](https://marketplace.visualstudio.com/items?itemname=redhat.vscode-yaml) extension for YAML language support.
2. Add the schema under the `yaml.schemas` key in your user or workspace [`settings.json`](https://code.visualstudio.com/docs/getstarted/settings):

```json
{
  "yaml.schemas": {
    "https://raw.githubusercontent.com/qgis-deployment/qgis-deployment-toolbelt-cli/refs/heads/main/docs/schemas/scenario/qdt_scenario.json": "*.qdt.yml"
  }
}
```

Alternatively you can add this line at the top of the file:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/qgis-deployment/qgis-deployment-toolbelt-cli/refs/heads/main/docs/schemas/scenario/qdt_scenario.json
```

----

## Using pre-commit

Since it's strongly recomended to use Git to store and publish QDT profiles and scenarios, it's possible to use git hooks to automatically validate QDT files.

Considering that your git project stores QDT profiles in a `profiles` subfolder and QDT scenarios in `scenarios` one, here comes a typical configuration for the [pre-commit micro-framework](https://pre-commit.com/) (see [upstream instructions](https://pre-commit.com/#install) to install it):

```{code-block} yaml
:caption: Example file .pre-commit-config.yaml (adapt to your subfolders)

exclude: ".venv|tests/dev/|tests/fixtures/"
fail_fast: false
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-yaml
      - id: detect-private-key
      - id: end-of-file-fixer
      - id: fix-byte-order-marker

  - repo: https://gitlab.com/bmares/check-json5
    rev: v1.0.0
    hooks:
      - id: check-json5

  - repo: https://github.com/python-jsonschema/check-jsonschema
    rev: 0.30.0
    hooks:
      - id: check-jsonschema
        name: Check QDT profiles
        files: ^profiles/.*\.json$
        args:
          - --schemafile
          - https://raw.githubusercontent.com/qgis-deployment/qgis-deployment-toolbelt-cli/main/docs/schemas/profile/qgis_profile.json

  - repo: https://github.com/python-jsonschema/check-jsonschema
    rev: 0.30.0
    hooks:
      - id: check-jsonschema
        name: Check QDT scenarios
        files: ^scenario/.*\.yml$
        args:
          - --default-filetype
          - yaml
          - --base-uri
          - https://raw.githubusercontent.com/qgis-deployment/qgis-deployment-toolbelt-cli/refs/heads/main/docs/schemas/scenario/
          - --schemafile
          - https://raw.githubusercontent.com/qgis-deployment/qgis-deployment-toolbelt-cli/refs/heads/main/docs/schemas/scenario/qdt_scenario.json
```
