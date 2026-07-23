"""Shared test configuration. Sets a strong JWT secret BEFORE importing the secure app,
so jwt_handler's fail-closed check is satisfied in the test environment."""
import os
import sys
import pathlib

os.environ.setdefault("JWT_SECRET", "test-secret-value-at-least-32-characters-long!!")

# Ensure the repo root is importable (common/, Chapter9/, Chapter12/ as namespace pkgs).
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def _reset_rate_limiter():
    """Clear the in-memory rate-limit window between tests."""
    from Chapter9.secure_api import rate_limit
    rate_limit.reset()
    yield
    rate_limit.reset()
