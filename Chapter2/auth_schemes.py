"""
Chapter 2 - Understanding APIs: access control schemes.
Illustrates the Authorization header formats for the schemes covered in the chapter.
"""
import base64
import hashlib
import hmac


def http_basic(username: str, password: str) -> str:
    raw = f"{username}:{password}".encode()
    return "Authorization: Basic " + base64.b64encode(raw).decode()


def bearer(token: str) -> str:
    return f"Authorization: Bearer {token}"


def api_key(key: str, header: str = "X-API-Key") -> str:
    return f"{header}: {key}"


def aws_keyed_hmac(secret: str, string_to_sign: str) -> str:
    """Simplified AWS-style signature: HMAC over a canonical request string."""
    sig = hmac.new(secret.encode(), string_to_sign.encode(), hashlib.sha256).hexdigest()
    return f"Authorization: AWS-HMAC-SHA256 Signature={sig}"


if __name__ == "__main__":
    print(http_basic("alice", "s3cr3t"))
    print(bearer("eyJhbGciOi..."))
    print(api_key("6f1e...c9"))
    print(aws_keyed_hmac("secretkey", "GET\n/things\n20240101"))
