# How to use

> TO DOC

----

## Using scenarios

This is the main way to use this toobelt. You write your deployment scenario by describing the steps to be done to prepare the QGIS environment, take a coffee (cup of tea is also tolerated)

The format used is YAML and the syntax is largely inspired by DevOPS oriented tools like Ansible or CI/CD platforms (GitHub Actions, GitLab CI in particular).

By default, the toolbelt will look for a file named `scenario.qdt.yml` in the current directory.  
If it is not found, it will expect subcommands to run.

### Sample scenario

For development and test purposes, project provides a [sample scenario](https://github.com/Guts/qgis-deployment-cli/blob/main/tests/fixtures/scenarios/good_scenario_sample.qdt.yml):

```{eval-rst}
.. literalinclude:: ../../tests/fixtures/scenarios/good_scenario_sample.qdt.yml
  :language: yaml
```

### Validate scenario using JSON Schema

In order to minimize friction and maximize productivity, the project tries to provide a [schema.json][https://json-schema.org/] for scenarios files. If your editor supports YAML schema validation, it's definitely recommended to set it up.

#### Generic

1. Ensure your editor of choice has support for YAML schema validation.
2. Add the following lines at the top of your scenario file:

``` yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/Guts/qgis-deployment-cli/main/docs/schemas/schema.json
```

#### Visual Studio Code

1. Install the [vscode-yaml][https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml] extension for YAML language support.
2. Add the schema under the `yaml.schemas` key in your user or workspace [`settings.json`][https://code.visualstudio.com/docs/getstarted/settings]:

``` json
{
  "yaml.schemas": {
    "https://raw.githubusercontent.com/Guts/qgis-deployment-cli/main/docs/schemas/schema.json": "*.qdt.yml"
  }
}
```

----

## As a CLI

To use as a CLI, make sure to remove any `scenario.qdt.yml` file from the current directory.

Then, you can use the following commands:

```bash
qdeploy-toolbelt --verbose check
qdeploy-toolbelt env-setup
```
