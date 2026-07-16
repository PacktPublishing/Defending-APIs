"""
Chapter 12 - Securing Microservices: the edge service.
Verifies the external caller's token at the edge (north-south auth), then mints a
short-lived, signed internal token for the downstream service (token propagation).
"""
import os
import time
import jwt
import requests
from fastapi import FastAPI, Header, HTTPException

# Separate trust domains: external tokens vs internal mesh tokens.
EXTERNAL_SECRET = os.environ.get("EXTERNAL_JWT_SECRET", "external-edge-secret-rotate-me")
INTERNAL_SECRET = os.environ.get("INTERNAL_JWT_SECRET", "internal-mesh-secret-rotate-me")
# Reach the orders service by its DNS name inside the mesh; overridable for local runs.
ORDERS_URL = os.environ.get("ORDERS_URL", "http://orders:12002")

app = FastAPI(title="gateway-service")


def verify_external(authorization: str) -> dict:
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(401, "authenticate at the edge")
    try:
        return jwt.decode(authorization.split(" ", 1)[1], EXTERNAL_SECRET,
                          algorithms=["HS256"], audience="edge")
    except jwt.PyJWTError:
        raise HTTPException(401, "invalid external token")


def mint_internal_token(user_id: str, scope: str) -> str:
    return jwt.encode(
        {"sub": user_id, "scope": scope, "exp": time.time() + 30,
         "iss": "gateway", "aud": "orders"},
        INTERNAL_SECRET, algorithm="HS256")


@app.get("/orders")
def list_orders(authorization: str = Header(default="")):
    claims = verify_external(authorization)          # actually authenticate the user
    internal = mint_internal_token(user_id=str(claims["sub"]), scope="orders:read")
    r = requests.get(f"{ORDERS_URL}/internal/orders",
                     headers={"Authorization": f"Bearer {internal}"}, timeout=5)
    return r.json()
