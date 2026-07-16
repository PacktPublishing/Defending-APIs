"""Unit tests for the hardened building blocks and validators."""
import os
import importlib
import pytest
import jwt
from Chapter8.validate_positive_model import validate_user
from Chapter12.services.orders_service import require_scope, INTERNAL_SECRET


def test_positive_model_accepts_valid():
    assert validate_user({"id": 1, "username": "alice"}) == []


def test_positive_model_rejects_mass_assignment_and_bad_types():
    errs = validate_user({"id": 0, "username": "bad name", "is_admin": True})
    assert any("unexpected" in e for e in errs)
    assert any("minimum" in e for e in errs)
    assert any("pattern" in e for e in errs)


def _internal(scope):
    return jwt.encode({"sub": "1", "scope": scope, "iss": "gateway", "aud": "orders"},
                      INTERNAL_SECRET, algorithm="HS256")


def test_scope_exact_membership():
    require_scope(f"Bearer {_internal('orders:read')}", "orders:read")  # ok


def test_scope_substring_does_not_satisfy():
    with pytest.raises(Exception):
        require_scope(f"Bearer {_internal('orders:reader')}", "orders:read")


def test_jwt_handler_fails_closed_without_secret(monkeypatch):
    monkeypatch.delenv("JWT_SECRET", raising=False)
    from Chapter9.secure_api import jwt_handler
    importlib.reload(jwt_handler)
    with pytest.raises(RuntimeError):
        jwt_handler.sign("1", "user")
    # restore
    monkeypatch.setenv("JWT_SECRET", "test-secret-value-at-least-32-characters-long!!")
    importlib.reload(jwt_handler)
