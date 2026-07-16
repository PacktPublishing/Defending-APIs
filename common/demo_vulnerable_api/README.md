# Demo Vulnerable API (shared target)

A tiny, **intentionally insecure** FastAPI application used across the attack and
defence chapters. Each flaw is annotated with its OWASP API Security Top 10 (2023) ID.

## Run

```bash
pip install -r ../../requirements.txt
uvicorn common.demo_vulnerable_api.app:app --reload --port 8000
# from the repo root
```

Then open http://localhost:8000/docs

## Built-in weaknesses

| Endpoint | Weakness | OWASP |
|----------|----------|-------|
| `/login` | Password never verified | API2 Broken Authentication |
| `/users/{id}` | No object ownership check + excessive fields | API1 BOLA / API3 |
| `/notes/{id}` | No object ownership check | API1 BOLA |
| `/admin/users` | Trusts forgeable `role` claim | API5 BFLA |
| `/search` | Unsanitised input into a query | API8 Injection |
| `/fetch` | Server-side request forgery sink | API7 SSRF |
| `/debug` | Verbose info disclosure | API8 Misconfiguration |
| JWT handling | Weak secret + signature not verified (`alg:none`) | API2 |

> Training use only. Never expose this on a network you do not control.
