# How to automatically validate profile.json and scenarios files


## Using pre-commit

Here comes a typical configuration:

```yaml
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
    rev: 0.28.0
    hooks:
      - id: check-jsonschema
        name: Check QDT profiles
        files: ^profiles/.*\.json$
        args:
          - --schemafile
          - https://raw.githubusercontent.com/Guts/qgis-deployment-cli/main/docs/schemas/profile/qgis_profile.json

  - repo: https://github.com/python-jsonschema/check-jsonschema
    rev: 0.28.0
    hooks:
      - id: check-jsonschema
        name: Check QDT scenarios
        files: ^qdt_scenarii/.*\.yml$
        args:
          - --default-filetype
          - yaml
          - --base-uri
          - https://raw.githubusercontent.com/Guts/qgis-deployment-cli/main/docs/schemas/scenario/
          - --schemafile
          - https://raw.githubusercontent.com/Guts/qgis-deployment-cli/main/docs/schemas/scenario/schema.json

```
