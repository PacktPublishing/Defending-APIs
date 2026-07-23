"""
Chapter 12 - Securing Microservices: a downstream service.
Only trusts internal tokens signed by the mesh secret, with the right audience and an
exact scope. This enforces east-west access control between services (internal zero-trust).
"""
import os
import jwt
from fastapi import FastAPI, Header, HTTPException

INTERNAL_SECRET = os.environ.get("INTERNAL_JWT_SECRET", "internal-mesh-secret-rotate-me")
app = FastAPI(title="orders-service")

ORDERS = [{"id": 1, "item": "book", "user": "1001"}]


def require_scope(authorization: str, scope: str) -> dict:
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(401)
    try:
        claims = jwt.decode(authorization.split(" ", 1)[1], INTERNAL_SECRET,
                            algorithms=["HS256"], audience="orders", issuer="gateway")
    except jwt.PyJWTError:
        raise HTTPException(401, "invalid internal token")
    # Parse the space-delimited scope string and require EXACT membership
    # (so "orders:reader" or "orders:read:all" do NOT satisfy "orders:read").
    granted = set(str(claims.get("scope", "")).split())
    if scope not in granted:
        raise HTTPException(403, "insufficient scope")
    return claims


@app.get("/internal/orders")
def internal_orders(authorization: str = Header(default="")):
    require_scope(authorization, "orders:read")
    return ORDERS
