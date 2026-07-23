"""
Chapter 5 - Foundations of Attacking APIs: interacting with an API.
A minimal requests-based client (the Python equivalent of the HTTPie/cURL examples).
"""
import requests

BASE = "http://localhost:8000"


def login(username: str) -> str:
    r = requests.post(f"{BASE}/login", json={"username": username, "password": "x"})
    r.raise_for_status()
    return r.json()["access_token"]


def get(path: str, token: str | None = None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return requests.get(f"{BASE}{path}", headers=headers, timeout=5)


if __name__ == "__main__":
    tok = login("bob")
    print("token:", tok[:24], "...")
    print("GET /users/2 ->", get("/users/2", tok).json())
