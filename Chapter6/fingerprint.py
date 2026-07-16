"""
Chapter 6 - Implementation analysis: OS/framework enumeration via response headers.
Passive fingerprinting from Server/X-Powered-By and error signatures.
"""
import requests

SIGNATURES = {
    "uvicorn": "ASGI (FastAPI/Starlette)",
    "gunicorn": "Python WSGI",
    "express": "Node.js Express",
    "nginx": "nginx reverse proxy",
    "kestrel": ".NET",
}


def fingerprint(url: str) -> dict:
    r = requests.get(url, timeout=5)
    server = (r.headers.get("server", "") + r.headers.get("x-powered-by", "")).lower()
    guesses = [v for k, v in SIGNATURES.items() if k in server]
    return {"server_header": r.headers.get("server"), "guesses": guesses or ["unknown"]}


if __name__ == "__main__":
    print(fingerprint("http://localhost:8000/"))
