"""
Chapter 9 - Handling JWTs securely.
The correct counterpart to the demo API's broken token handling: strong secret,
explicit algorithm allow-list, and full verification of signature, exp, iss and aud.
"""
import os
import time
import jwt

ALG = "HS256"
ISSUER, AUDIENCE = "defending-apis", "defending-apis-clients"


def _secret() -> str:
    """Fail closed: never fall back to a hard-coded or committed secret."""
    secret = os.environ.get("JWT_SECRET")
    if not secret or len(secret) < 32:
        raise RuntimeError(
            "JWT_SECRET must be set to a random value of at least 32 characters. "
            "Refusing to sign/verify with a weak or default key.")
    return secret


def sign(user_id: str, role: str, ttl: int = 600) -> str:
    now = int(time.time())
    payload = {"sub": user_id, "role": role, "iat": now, "exp": now + ttl,
               "iss": ISSUER, "aud": AUDIENCE}
    return jwt.encode(payload, _secret(), algorithm=ALG)


def verify(token: str) -> dict:
    # algorithms allow-list defeats alg:none; audience/issuer checks defeat token reuse.
    return jwt.decode(token, _secret(), algorithms=[ALG],
                      audience=AUDIENCE, issuer=ISSUER,
                      options={"require": ["exp", "iat", "sub"]})


if __name__ == "__main__":
    os.environ.setdefault("JWT_SECRET", "demo-only-set-a-real-32char-secret-here!")
    t = sign("1001", "user")
    print("verified claims:", verify(t))
