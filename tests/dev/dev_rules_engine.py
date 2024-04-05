import pprint
from sys import platform

from python_rule_engine import RuleEngine

# rule = {
#     "name": "basic_rule",
#     "conditions": {
#         "all": [
#             {
#                 # JSONPath support
#                 "path": "$.person.name",
#                 "operator": "equal",
#                 "value": "Lionel",
#             },
#             {"path": "$.person.last_name", "operator": "equal", "value": "Messi"},
#             {
#                 "path": "$.environment.name",
#                 "operator": "equal",
#                 "value": "linux",
#             },
#         ]
#     },
# }

# print(platform)
# obj = {
#     "person": {"name": "Lionel", "last_name": "Messi"},
#     "environment": {"name": platform},
# }

# engine = RuleEngine([rule])

# results = engine.evaluate(obj)
# # print(all([r.conditions.match for r in results]))
# print(len(results))
# for r in results:
#     print(r)
#     print(r.description)
#     print(r.conditions.match)

#  from package tests
obj = {
    "person": {"name": "Santissago", "last_name": "Alvarez"},
    "environment": {"operating_system": platform},
}

rules = [
    {
        "name": "basic_rule",
        "description": "Basic rule to test the engine",
        "extra": {"some_field": "some_value"},
        "conditions": {
            "all": [
                {
                    "condition": "pioupiou",
                    "path": "$.person.name",
                    "value": "Santiago",
                    "operator": "equal",
                },
                {"path": "$.person.last_name", "value": "Alvarez", "operator": "equal"},
            ]
        },
    },
    {
        "name": "basic_rule",
        "description": "Basic rule to test the engine",
        "extra": {"some_field": "some_value"},
        "conditions": {
            "all": [
                {
                    "path": "$.environment.operating_system",
                    "value": "linux",
                    "operator": "equal",
                },
            ]
        },
    },
]

engine = RuleEngine(rules)

results = engine.evaluate(obj)
print(f"{len(rules)} rules")
print(len(results), [r.conditions.match for r in results])
if len(results) == len(rules):
    assert results[0].conditions.match is True
else:
    print("FAIIILED")
