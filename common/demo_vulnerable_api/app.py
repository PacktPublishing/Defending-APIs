"""
demo_vulnerable_api — an intentionally INSECURE API used as a training target.

Do NOT deploy this. It exists so the attack chapters (5-7) have something to hit and
the defence chapters (8-12) have a concrete "before" to fix. Each vulnerability is
labelled with the relevant OWASP API Security Top 10 (2023) identifier.

Run:
    uvicorn common.demo_vulnerable_api.app:app --reload --port 8000
"""
from __future__ import annotations

import time
import jwt
from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel

# --- Deliberately weak configuration -----------------------------------------
# API1:2023 / auth weaknesses: a short, guessable HMAC secret and a permissive alg.
WEAK_SECRET = "secret"          # trivially brute-forceable (see Chapter 5/7)
JWT_ALG = "HS256"

app = FastAPI(title="Demo Vulnerable API", version="0.1.0")

# In-memory "database" -- note user 1 is an admin.
USERS = {
    1: {"id": 1, "username": "alice", "role": "admin",
        "email": "alice@example.com", "ssn": "111-11-1111", "balance": 4200},
    2: {"id": 2, "username": "bob", "role": "user",
        "email": "bob@example.com", "ssn": "222-22-2222", "balance": 15},
    3: {"id": 3, "username": "carol", "role": "user",
        "email": "carol@example.com", "ssn": "333-33-3333", "balance": 980},
}
NOTES = {1: "alice private note", 2: "bob private note", 3: "carol private note"}


def make_token(user_id: int) -> str:
    """Issue a token. Intentionally uses a weak secret and no audience/issuer."""
    payload = {"sub": user_id, "role": USERS[user_id]["role"],
               "exp": time.time() + 3600}
    return jwt.encode(payload, WEAK_SECRET, algorithm=JWT_ALG)


def current_user(authorization: str | None) -> dict:
    """
    VULNERABLE token handling:
      - accepts alg:none (no signature) because verification is sloppy
      - uses the weak shared secret
    """
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(401, "missing bearer token")
    token = authorization.split(" ", 1)[1]
    try:
        # BUG: verify_signature disabled allows tampering / alg:none forgery.
        claims = jwt.decode(token, options={"verify_signature": False})
    except jwt.PyJWTError:
        raise HTTPException(401, "bad token")
    uid = int(claims.get("sub", 0))
    if uid not in USERS:
        raise HTTPException(401, "unknown user")
    # BUG: trusts the role claim from the (unverified) token.
    return {**USERS[uid], "role": claims.get("role", USERS[uid]["role"])}


class Login(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(body: Login):
    # API2:2023 broken authentication: password is never actually checked.
    for u in USERS.values():
        if u["username"] == body.username:
            return {"access_token": make_token(u["id"]), "token_type": "bearer"}
    raise HTTPException(401, "no such user")


@app.get("/users/{user_id}")
def get_user(user_id: int, authorization: str | None = Header(default=None)):
    current_user(authorization)  # authenticated...
    # API1:2023 BOLA: ...but never checks the token owner matches user_id,
    # and returns excessive fields (ssn, balance) -- API3:2023.
    if user_id not in USERS:
        raise HTTPException(404, "not found")
    return USERS[user_id]


@app.get("/notes/{user_id}")
def get_note(user_id: int, authorization: str | None = Header(default=None)):
    current_user(authorization)
    # API1:2023 BOLA on a second resource.
    return {"user_id": user_id, "note": NOTES.get(user_id, "")}


@app.get("/admin/users")
def admin_list(authorization: str | None = Header(default=None)):
    user = current_user(authorization)
    # API5:2023 BFLA: relies only on the forgeable role claim.
    if user["role"] != "admin":
        raise HTTPException(403, "admins only")
    return list(USERS.values())


@app.get("/search")
def search(q: str):
    # API8:2023 injection: naive string handling; the attack samples show how a
    # real backend concatenating this into SQL/NoSQL/shell would be exploitable.
    fake_sql = f"SELECT * FROM users WHERE username = '{q}'"
    return {"executed_query": fake_sql,
            "results": [u for u in USERS.values() if q in u["username"]]}


@app.get("/fetch")
def fetch(url: str):
    # API7:2023 SSRF: echoes back the target it *would* request. The real risk is
    # that a server making this request could reach internal metadata endpoints.
    return {"would_request": url,
            "warning": "SSRF sink -- a real server would fetch this URL"}


@app.get("/debug")
def debug(request: Request):
    # API8:2023 misconfiguration: leaks environment/headers verbosely.
    return {"headers": dict(request.headers), "client": request.client.host}


@app.get("/")
def root():
    return {"status": "ok", "service": "demo-vulnerable-api",
            "warning": "intentionally insecure -- training use only"}
