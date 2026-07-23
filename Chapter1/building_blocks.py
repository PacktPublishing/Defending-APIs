"""
Chapter 1 - What Is API Security?
Demonstrates the core API "building blocks" from the chapter: hashing, HMAC,
signatures, encoding, and transport-security concepts.
"""
import base64
import hashlib
import hmac
import secrets


def hashing_demo(message: bytes = b"Learn about API security") -> str:
    """A hash is a one-way fingerprint of data (integrity check)."""
    return hashlib.sha256(message).hexdigest()


def hmac_demo(message: bytes, key: bytes) -> str:
    """An HMAC binds a hash to a secret key (integrity + authenticity)."""
    return hmac.new(key, message, hashlib.sha256).hexdigest()


def encoding_demo(message: bytes) -> dict:
    """Encoding is NOT encryption -- base64 is reversible by anyone."""
    b64 = base64.b64encode(message).decode()
    return {"encoded": b64, "decoded": base64.b64decode(b64).decode()}


def constant_time_compare(a: str, b: str) -> bool:
    """Avoid timing attacks when comparing secrets/signatures."""
    return hmac.compare_digest(a, b)


if __name__ == "__main__":
    key = secrets.token_bytes(32)
    msg = b"Learn about API security"
    print("SHA-256 :", hashing_demo(msg))
    sig = hmac_demo(msg, key)
    print("HMAC    :", sig)
    print("Encoding:", encoding_demo(msg))
    print("Verify  :", constant_time_compare(sig, hmac_demo(msg, key)))
