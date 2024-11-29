#! python3  # noqa: E265

# libraries
import json
import os
from pprint import pprint
from urllib.parse import urljoin

import jsonref
import jsonschema


def add_local_schemas_to(resolver, schema_folder, base_uri, schema_ext=".schema.json"):
    """Add local schema instances to a resolver schema cache.

    Arguments:
        resolver (jsonschema.RefResolver): the reference resolver
        schema_folder (str): the local folder of the schemas.
        base_uri (str): the base URL that you actually use in your '$id' tags
            in the schemas
        schema_ext (str): filter files with this extension in the schema_folder
    """
    for dir, _, files in os.walk(schema_folder):
        for file in files:
            if file.endswith(schema_ext):
                schema_path = Path(dir) / Path(file)
                rel_path = schema_path.relative_to(schema_folder)
                with open(schema_path) as schema_file:
                    schema_doc = json.load(schema_file)
                key = urljoin(base_uri, str(rel_path))
                resolver.store[key] = schema_doc


reader = ScenarioReader(Path("tests/fixtures/scenarios/good_scenario_sample.qdt.yml"))
# pprint(reader.scenario)

schema = Path("docs/schemas/schema.json")
print(schema.is_file())
# with schema.open("r") as s:
#     d = jsonref.loads(s.read())
# # print(d)

with schema.open("r") as s:
    schema_data = json.load(s)
# print(schema_data)

# json_ref_resolver = jsonschema.RefResolver(
#     referrer=schema_data, base_uri="file://" + str(schema.parent.resolve) + "/"
# )

# jsonschema.validate(
#     instance=reader.scenario,
#     schema=str(schema.resolve()),
#     resolver=json_ref_resolver,
# )

instance_data = reader.scenario
schema_folder = Path("docs/schemas/")
schema_filename = schema_folder / "schema.json"
base_uri = "https://raw.githubusercontent.com/qgis-deployment/qgis-deployment-toolbelt-cli/feature/scenario-pseudo-ci/docs/schemas/"

resolver = jsonschema.RefResolver(base_uri=base_uri, referrer=schema_data)
add_local_schemas_to(resolver, schema_folder, base_uri)
print(dir(resolver))
jsonschema.validate(instance_data, schema_data, resolver=resolver)
