import json
from jsonschema import Draft202012Validator


def load_schema(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_items(items, schema):
    validator = Draft202012Validator(schema)
    for i, item in enumerate(items):
        errors = sorted(validator.iter_errors(item), key=lambda e: e.path)
        if errors:
            return i, [e.message for e in errors]
    return None, None
