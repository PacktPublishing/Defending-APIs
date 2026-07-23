"""
Chapter 9 - Authorization middleware (object- and function-level).
FastAPI dependencies that enforce BOLA/BFLA protection the demo API lacks.
"""
from fastapi import Depends, Header, HTTPException
from . import jwt_handler


def current_user(authorization: str = Header(default="")) -> dict:
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(401, "missing bearer token")
    try:
        claims = jwt_handler.verify(authorization.split(" ", 1)[1])
    except Exception:
        raise HTTPException(401, "invalid token")
    return {"id": int(claims["sub"]), "role": claims["role"]}


def require_owner(user_id: int, user: dict = Depends(current_user)) -> dict:
    # Object-level: the caller may only act on their own resource (defeats BOLA).
    if user["id"] != user_id and user["role"] != "admin":
        raise HTTPException(403, "not the resource owner")
    return user


def require_role(role: str):
    # Function-level: explicit role check on the server (defeats BFLA).
    def _dep(user: dict = Depends(current_user)) -> dict:
        if user["role"] != role:
            raise HTTPException(403, f"requires role {role}")
        return user
    return _dep
