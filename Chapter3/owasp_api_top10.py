"""
Chapter 3 - Understanding Common API Vulnerabilities.
A compact FastAPI app with one endpoint per OWASP API Security Top 10 (2023) item,
each annotated to explain the root cause. Deliberately vulnerable -- study, don't ship.

Run: uvicorn owasp_api_top10:app --reload
"""
from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI(title="OWASP API Top 10 (2023) examples")

DB = {1: {"owner": "alice", "secret": "A"}, 2: {"owner": "bob", "secret": "B"}}
INVENTORY = {"/api/v1/users": "current", "/api/v0/users": "deprecated-but-live"}


@app.get("/api1/object/{oid}")
def api1_bola(oid: int, user: str = Header(default="bob")):
    # API1 Broken Object Level Authorization: no check that `user` owns `oid`.
    return DB.get(oid, {})


@app.get("/api2/whoami")
def api2_broken_auth(token: str = ""):
    # API2 Broken Authentication: accepts any non-empty token.
    if not token:
        raise HTTPException(401)
    return {"ok": True}


@app.post("/api3/user")
def api3_property_level(payload: dict):
    # API3 Broken Object Property Level Authorization: blindly trusts client fields,
    # allowing privilege escalation via e.g. {"is_admin": true}.
    return {"created": payload}


@app.get("/api4/report")
def api4_resource_consumption(rows: int = 1000000):
    # API4 Unrestricted Resource Consumption: no upper bound on `rows`.
    return {"generating_rows": rows}


@app.get("/api5/admin")
def api5_bfla(role: str = "user"):
    # API5 Broken Function Level Authorization: trusts a client-supplied role.
    return {"admin_data": role == "admin"}


@app.post("/api6/transfer")
def api6_sensitive_flow(amount: float, to: str):
    # API6 Unrestricted Access to Sensitive Business Flows: a money-transfer flow
    # with no rate limiting, bot protection or step-up auth -- ripe for automation abuse.
    return {"transferred": amount, "to": to}


@app.get("/api7/fetch")
def api7_ssrf(url: str):
    # API7 Server Side Request Forgery: the server would fetch an attacker-supplied URL,
    # potentially reaching internal metadata endpoints (169.254.169.254, etc.).
    return {"would_request": url}


@app.get("/api8/debug")
def api8_misconfiguration(request: Request):
    # API8 Security Misconfiguration: verbose debug output leaks internals.
    return {"headers": dict(request.headers), "stack_trace_enabled": True}


@app.get("/api9/inventory")
def api9_improper_inventory():
    # API9 Improper Inventory Management: an old, undocumented API version is still live.
    return INVENTORY


@app.get("/api10/aggregate")
def api10_unsafe_consumption(third_party_url: str = "http://partner.example/data"):
    # API10 Unsafe Consumption of APIs: blindly trusts data from an upstream third party
    # without validation, so a compromised partner can inject malicious responses.
    return {"trusted_without_validation": third_party_url}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
