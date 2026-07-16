"""Confirms the demo API is vulnerable as designed (the 'before' picture)."""
import jwt
from fastapi.testclient import TestClient
from common.demo_vulnerable_api.app import app

client = TestClient(app)


def _forge(user_id, role):
    return jwt.encode({"sub": user_id, "role": role}, "secret", algorithm="HS256")


def test_login_ignores_password():
    r = client.post("/login", json={"username": "bob", "password": "anything"})
    assert r.status_code == 200 and "access_token" in r.json()


def test_bola_reads_other_users_record():
    tok = _forge(2, "user")  # logged in as bob...
    r = client.get("/users/1", headers={"Authorization": f"Bearer {tok}"})
    assert r.status_code == 200            # ...but can read alice's record (BOLA)
    assert r.json()["ssn"] == "111-11-1111"  # and excessive data is exposed


def test_bfla_forged_admin_reaches_admin_endpoint():
    tok = _forge(2, "admin")  # bob forges an admin role claim
    r = client.get("/admin/users", headers={"Authorization": f"Bearer {tok}"})
    assert r.status_code == 200 and len(r.json()) == 3
