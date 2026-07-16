"""
Chapter 6 - Discovering APIs: active enumeration.
Word-list driven endpoint discovery -- probes common API paths and reports live ones.
"""
import requests

BASE = "http://localhost:8000"
WORDLIST = ["/", "/login", "/users/1", "/notes/1", "/admin/users",
            "/search?q=a", "/fetch?url=x", "/debug", "/health", "/v1/users"]


def discover(base: str = BASE):
    for path in WORDLIST:
        try:
            r = requests.get(base + path, timeout=3)
            print(f"{r.status_code:>3}  {path}")
        except requests.RequestException as e:
            print(f"ERR  {path}  ({e.__class__.__name__})")


if __name__ == "__main__":
    discover()
