"""
Chapter 9 - Defending against Common Vulnerabilities.
The secure reference API wiring together the hardened building blocks. Compare each
endpoint with common/demo_vulnerable_api/app.py to see the fix.

Requires JWT_SECRET to be set (see jwt_handler.py -- it fails closed without one).
Run: JWT_SECRET=$(openssl rand -hex 32) uvicorn Chapter9.secure_api.app:app --port 9000
"""
from fastapi import Depends, FastAPI, HTTPException
from .authz import current_user, require_owner, require_role
from .schemas import UserPublic, UserCreate
from .rate_limit import rate_limiter
from . import passwords

# Apply rate limiting globally as a router-level dependency (API4 protection).
app = FastAPI(title="Secure Reference API", dependencies=[Depends(rate_limiter)])

DB = {
    1: {"id": 1, "username": "alice", "role": "admin", "email": "alice@example.com",
        "ssn": "111-11-1111", "balance": 4200},
    2: {"id": 2, "username": "bob", "role": "user", "email": "bob@example.com",
        "ssn": "222-22-2222", "balance": 15},
}


@app.get("/users/{user_id}", response_model=UserPublic)
def get_user(user_id: int, _: dict = Depends(require_owner)):
    # BOLA fixed by require_owner; excessive exposure fixed by response_model.
    if user_id not in DB:
        raise HTTPException(404)
    return DB[user_id]


@app.post("/users", response_model=UserPublic, status_code=201)
def create_user(body: UserCreate):
    # Mass assignment blocked by UserCreate(extra=forbid); password is hashed.
    new_id = max(DB) + 1
    DB[new_id] = {"id": new_id, "username": body.username, "role": "user",
                  "email": body.email, "pw": passwords.hash_password(body.password)}
    return DB[new_id]


@app.get("/admin/users", response_model=list[UserPublic])
def admin_users(_: dict = Depends(require_role("admin"))):
    # BFLA fixed: role verified server-side from a fully-verified token.
    return list(DB.values())
