"""
Chapter 8 - Leveraging the positive security model.
Validates an incoming payload against the constraints declared in Chapter8/openapi.yaml:
required fields, types, numeric bounds, string patterns/length, email format, and a
strict field allow-list (reject anything not explicitly permitted). This is the essence
of shift-left -- enforce the contract, deny by default.
"""
import re

USERNAME_RE = re.compile(r"^[a-zA-Z0-9_]{1,64}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# Mirrors components.schemas.User in Chapter8/openapi.yaml.
SCHEMA = {
    "required": ["id", "username"],
    "additionalProperties": False,
    "properties": {
        "id": {"type": int, "min": 1, "max": 1_000_000},
        "username": {"type": str, "pattern": USERNAME_RE},
        "email": {"type": str, "format": EMAIL_RE},
    },
}


def validate_user(payload: dict) -> list[str]:
    errors: list[str] = []
    props = SCHEMA["properties"]

    for field in SCHEMA["required"]:
        if field not in payload:
            errors.append(f"missing required field: {field}")

    if not SCHEMA["additionalProperties"]:
        extra = set(payload) - set(props)
        if extra:
            errors.append(f"unexpected fields (possible mass assignment): {sorted(extra)}")

    for field, spec in props.items():
        if field not in payload:
            continue
        value = payload[field]
        if not isinstance(value, spec["type"]) or isinstance(value, bool):
            errors.append(f"{field}: expected {spec['type'].__name__}")
            continue
        if "min" in spec and value < spec["min"]:
            errors.append(f"{field}: below minimum {spec['min']}")
        if "max" in spec and value > spec["max"]:
            errors.append(f"{field}: above maximum {spec['max']}")
        if "pattern" in spec and not spec["pattern"].match(value):
            errors.append(f"{field}: fails allow-list pattern")
        if "format" in spec and not spec["format"].match(value):
            errors.append(f"{field}: invalid format")
    return errors


if __name__ == "__main__":
    cases = {
        "valid": {"id": 1, "username": "alice", "email": "a@example.com"},
        "mass-assignment": {"id": 1, "username": "alice", "is_admin": True},
        "bad-types-and-bounds": {"id": 0, "username": "has spaces", "email": "nope"},
        "missing-required": {"email": "a@example.com"},
    }
    for name, payload in cases.items():
        print(f"{name}: {validate_user(payload) or 'accepted'}")
