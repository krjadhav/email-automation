import json

from jsonschema import ValidationError, validate


def load_rules(filename):
    schema = {
        "type": "object",
        "properties": {
            "rules": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "predicate": {"type": "string", "enum": ["All", "Any"]},
                        "conditions": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "field": {
                                        "type": "string",
                                        "enum": [
                                            "From",
                                            "To",
                                            "Subject",
                                            "Received Date",
                                        ],
                                    },
                                    "predicate": {
                                        "type": "string",
                                        "enum": [
                                            "contains",
                                            "not contains",
                                            "equals",
                                            "does not equal",
                                            "less than",
                                            "greater than",
                                        ],
                                    },
                                    "value": {"type": "string"},
                                },
                                "required": ["field", "predicate", "value"],
                            },
                        },
                        "actions": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {"action": {"type": "string"}},
                                "required": ["action"],
                            },
                        },
                    },
                    "required": ["predicate", "conditions", "actions"],
                },
            }
        },
        "required": ["rules"],
    }

    # Load and validate the rules JSON file
    with open(filename) as f:
        rules_data = json.load(f)

    try:
        validate(rules_data, schema)
        return rules_data["rules"]
    except ValidationError as e:
        print(f"Invalid rules.json file: {e}")
        return None
