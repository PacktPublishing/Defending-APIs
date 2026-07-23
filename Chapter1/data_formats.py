"""
Chapter 1 - Examining API data formats.
Round-trips the same record through JSON, YAML and XML to show the trade-offs.
"""
import json
import xml.etree.ElementTree as ET

import yaml  # PyYAML

RECORD = {"to": "Colin", "priority": "High",
          "heading": "Reminder", "body": "Learn about API security"}


def as_json(record: dict) -> str:
    return json.dumps(record, indent=2)


def as_yaml(record: dict) -> str:
    return yaml.safe_dump(record, sort_keys=False)


def as_xml(record: dict, root: str = "note") -> str:
    el = ET.Element(root)
    for k, v in record.items():
        child = ET.SubElement(el, k)
        child.text = str(v)
    return ET.tostring(el, encoding="unicode")


if __name__ == "__main__":
    print("JSON:\n", as_json(RECORD))
    print("\nYAML:\n", as_yaml(RECORD))
    print("\nXML:\n", as_xml(RECORD))
