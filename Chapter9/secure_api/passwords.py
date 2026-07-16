"""
Chapter 9 - Password and token hardening.
Uses bcrypt via passlib (slow, salted) and a CSPRNG for reset tokens.
"""
import secrets
from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    return pwd.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd.verify(plain, hashed)


def new_reset_token(nbytes: int = 32) -> str:
    # Cryptographically secure, high-entropy, URL-safe reset token.
    return secrets.token_urlsafe(nbytes)


if __name__ == "__main__":
    h = hash_password("correct horse battery staple")
    print("hash:", h)
    print("verify ok  :", verify_password("correct horse battery staple", h))
    print("verify bad :", verify_password("wrong", h))
    print("reset token:", new_reset_token())
