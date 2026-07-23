"""Confirms the Chapter 9 secure API fixes each vulnerability (the 'after' picture)."""
import jwt
from fastapi.testclient import TestClient
from Chapter9.secure_api.app import app
from Chapter9.secure_api import jwt_handler

client = TestClient(app)


def _valid(user_id, role):
    return jwt_handler.sign(str(user_id), role)


def test_unsigned_alg_none_token_rejected():
    forged = jwt.encode({"sub": 2, "role": "admin"}, key="", algorithm="none")
    r = client.get("/admin/users", headers={"Authorization": f"Bearer {forged}"})
    assert r.status_code == 401


def test_wrong_secret_token_rejected():
    bad = jwt.encode({"sub": 2, "role": "admin"}, "secret", algorithm="HS256")
    r = client.get("/admin/users", headers={"Authorization": f"Bearer {bad}"})
    assert r.status_code == 401


def test_bola_blocked_for_non_owner():
    tok = _valid(2, "user")
    assert client.get("/users/1", headers={"Authorization": f"Bearer {tok}"}).status_code == 403
    assert client.get("/users/2", headers={"Authorization": f"Bearer {tok}"}).status_code == 200


def test_response_model_strips_sensitive_fields():
    tok = _valid(2, "user")
    body = client.get("/users/2", headers={"Authorization": f"Bearer {tok}"}).json()
    assert "ssn" not in body and "balance" not in body


def test_bfla_requires_real_admin_role():
    assert client.get("/admin/users",
                      headers={"Authorization": f"Bearer {_valid(2, 'user')}"}).status_code == 403
    assert client.get("/admin/users",
                      headers={"Authorization": f"Bearer {_valid(1, 'admin')}"}).status_code == 200


def test_mass_assignment_rejected():
    r = client.post("/users", json={"username": "eve", "email": "e@x.com",
                                    "password": "pw", "is_admin": True})
    assert r.status_code == 422  # extra field forbidden by UserCreate
