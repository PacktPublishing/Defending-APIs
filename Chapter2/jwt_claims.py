"""
Chapter 2 - Using JWTs for claims and identity.
Shows how a signed JWT is created, decoded and verified with the standard claims.
"""
import time
import jwt

SECRET = "a-reasonably-long-demo-secret-value"


def issue(user_id: str, role: str, ttl: int = 600) -> str:
    now = int(time.time())
    payload = {"sub": user_id, "role": role, "iat": now,
               "exp": now + ttl, "iss": "demo-issuer", "aud": "demo-api"}
    return jwt.encode(payload, SECRET, algorithm="HS256")


def verify(token: str) -> dict:
    return jwt.decode(token, SECRET, algorithms=["HS256"],
                      audience="demo-api", issuer="demo-issuer")


if __name__ == "__main__":
    t = issue("1001", "user")
    print("token :", t)
    print("claims:", verify(t))
