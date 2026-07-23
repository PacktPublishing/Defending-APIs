"""
Chapter 4 - Investigating Recent Breaches.
Reproduces the *pattern* (not any real system) behind two of the breaches discussed:
  1. BOLA on a sequential object id (e.g. the campus access-control case).
  2. An unauthenticated admin/info endpoint (e.g. the smart-scale case).
These run entirely locally against a stub to illustrate the root cause safely.
"""
from dataclasses import dataclass, field


@dataclass
class StubServer:
    """A stand-in for a real backend, showing the flawed authorisation logic."""
    records: dict = field(default_factory=lambda: {
        i: {"owner_id": i, "pii": f"user-{i}-data"} for i in range(1, 6)})

    def get_record(self, record_id: int, caller_id: int):
        # FLAW: returns any record regardless of who is asking (BOLA).
        return self.records.get(record_id)

    def admin_info(self, token: str | None):
        # FLAW: no authentication required at all.
        return {"firmware": "1.0", "wifi_ssid": "HomeNet", "users": len(self.records)}


def demonstrate():
    s = StubServer()
    print("Attacker (id=2) enumerating other users' records via BOLA:")
    for rid in s.records:
        print(f"  record {rid} ->", s.get_record(rid, caller_id=2))
    print("Unauthenticated admin info leak:", s.admin_info(token=None))


if __name__ == "__main__":
    demonstrate()
