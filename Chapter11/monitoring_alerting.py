"""
Chapter 11 - API monitoring and alerting.
Tails a stream of access-log records and raises alerts on abuse signals
(auth failures, BOLA-style enumeration, rate spikes) discussed in the chapter.
"""
from collections import defaultdict

# (client_ip, status, path)
SAMPLE_LOG = [
    ("10.0.0.9", 401, "/login"), ("10.0.0.9", 401, "/login"),
    ("10.0.0.9", 401, "/login"), ("10.0.0.9", 200, "/users/1"),
    ("10.0.0.9", 200, "/users/2"), ("10.0.0.9", 200, "/users/3"),
    ("10.0.0.9", 200, "/users/4"),
]

AUTH_FAIL_THRESHOLD = 3
ENUM_THRESHOLD = 4


def analyse(log):
    auth_fails = defaultdict(int)
    object_hits = defaultdict(set)
    alerts = []
    for ip, status, path in log:
        if status == 401:
            auth_fails[ip] += 1
            if auth_fails[ip] == AUTH_FAIL_THRESHOLD:
                alerts.append(f"[BRUTE-FORCE] {ip}: {AUTH_FAIL_THRESHOLD} auth failures")
        if path.startswith("/users/") and status == 200:
            object_hits[ip].add(path)
            if len(object_hits[ip]) == ENUM_THRESHOLD:
                alerts.append(f"[BOLA?] {ip}: enumerated {ENUM_THRESHOLD} distinct objects")
    return alerts


if __name__ == "__main__":
    for a in analyse(SAMPLE_LOG):
        print(a)
