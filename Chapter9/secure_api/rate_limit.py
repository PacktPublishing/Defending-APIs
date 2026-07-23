"""
Chapter 9 - Protecting against unrestricted resource consumption.
A minimal in-memory sliding-window rate limiter, exposed as a FastAPI dependency.
Use a shared store (e.g. Redis) in production.
"""
import time
from collections import defaultdict, deque
from fastapi import HTTPException, Request

_WINDOW, _MAX = 60, 20            # 20 requests per 60 seconds per client
_hits: dict[str, deque] = defaultdict(deque)


def check(client_id: str) -> None:
    now = time.time()
    q = _hits[client_id]
    while q and q[0] <= now - _WINDOW:
        q.popleft()
    if len(q) >= _MAX:
        raise HTTPException(429, "rate limit exceeded")
    q.append(now)


def rate_limiter(request: Request) -> None:
    """FastAPI dependency: throttle per client IP."""
    check(request.client.host if request.client else "unknown")


def reset() -> None:
    """Test helper to clear the window."""
    _hits.clear()


if __name__ == "__main__":
    for i in range(22):
        try:
            check("tester")
        except HTTPException:
            print(f"request {i}: rate limited")
            break
    else:
        print("all requests allowed")
