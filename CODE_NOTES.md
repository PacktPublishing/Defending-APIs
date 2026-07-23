# About this code

These samples accompany *Defending APIs* (Colin Domoney, Packt, 2024).

They are compact, illustrative samples for the ideas in each chapter. They are a
starting point for readers to extend and experiment with. They are **not**
production-ready. The attack and vulnerable samples are intentionally insecure.

> Portions of this sample code were generated with AI assistance and reviewed by
> the author. Use them for learning only.

## The big picture

Two FastAPI apps sit at the centre of the runnable samples:

| App | Path | Role |
|-----|------|------|
| Demo vulnerable API | `common/demo_vulnerable_api/` | Shared target for attack chapters (5–7). Deliberately broken. |
| Secure reference API | `Chapter9/secure_api/` | Hardened counterpart. Same kinds of endpoints, fixed. |

Chapters 5–7 show attacks against the vulnerable app. Chapter 9 shows how those
same classes of flaw are closed. Chapters 8 and 10–12 build further defence
ideas (contracts, gateways, microservices) on top of that story.

Each chapter folder also has smaller standalone scripts. See that chapter's
`README.md` for what each file is for.

## Setup

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install pytest httpx           # needed for the test suite
```

Python 3.10+ is required.

## Running the two APIs

Always run these commands from the **repository root** so Python can import
`common` and `Chapter9`.

Vulnerable demo (port 8000):

```bash
uvicorn common.demo_vulnerable_api.app:app --reload --port 8000
```

Open http://localhost:8000/docs

Secure Chapter 9 API (port 9000). It refuses to start without a real secret:

```bash
JWT_SECRET=$(python -c "import secrets;print(secrets.token_hex(32))") \
  uvicorn Chapter9.secure_api.app:app --reload --port 9000
```

Open http://localhost:9000/docs

## Tests: what they are and how to run them

The suite in `tests/` checks both sides of the story with FastAPI's `TestClient`.
It does **not** start a server. Pytest loads the app modules directly and sends
HTTP requests in-process.

### Why the command does not say `Chapter9`

A command like this:

```bash
pytest tests/test_secure_api.py -v
```

never mentions `Chapter9` in the path. That is expected. The connection is
inside the test file:

```python
from Chapter9.secure_api.app import app
```

So: pytest runs the *test file*; the test file imports and exercises the
Chapter 9 app. Same idea for the vulnerable API:

```python
from common.demo_vulnerable_api.app import app
```

### "Attack fails" means "test passes"

For the secure API tests, a green result means the *attack did not work*.

Example: `test_bola_blocked_for_non_owner` passes when Bob gets `403` trying to
read Alice's record. The security control succeeded; therefore the test passed.

The vulnerable-API tests work the other way: they pass when the attack *does*
work (password ignored, BOLA allowed, forged admin role accepted). That is how
we keep the demo API intentionally broken.

### Which file tests what

| Test file | Imports / exercises | What a pass means |
|-----------|---------------------|-------------------|
| `tests/test_vulnerable_api.py` | `common.demo_vulnerable_api.app` | Known flaws still exploitable |
| `tests/test_secure_api.py` | `Chapter9.secure_api.app` | Same attack patterns are blocked |
| `tests/test_units.py` | Chapter 8 positive-model validator; Chapter 12 scope check; Chapter 9 JWT fail-closed | Building-block behaviour is correct |

### Why `JWT_SECRET` is on the command line

`Chapter9/secure_api/jwt_handler.py` fails closed if `JWT_SECRET` is missing. The
secure-API tests (and anything that imports that module) need it set. The
vulnerable-API tests do not care about the value, but setting it for the full
suite is simplest.

`tests/conftest.py` also sets a default for local runs. Prefer exporting a
fresh secret yourself so the command matches what CI does.

### Commands

Full suite (what CI runs):

```bash
pip install -r requirements.txt pytest httpx
JWT_SECRET=$(python -c "import secrets;print(secrets.token_hex(32))") pytest -q
```

Expect **14 passed**. A `passlib` / `crypt` deprecation warning on Python 3.12
is harmless noise from a dependency.

Chapter 9 only:

```bash
JWT_SECRET=$(python -c "import secrets;print(secrets.token_hex(32))") \
  pytest tests/test_secure_api.py -v
```

Vulnerable demo only:

```bash
pytest tests/test_vulnerable_api.py -v
```

Units (Chapters 8, 9, and 12 building blocks):

```bash
JWT_SECRET=$(python -c "import secrets;print(secrets.token_hex(32))") \
  pytest tests/test_units.py -v
```

## Safety / ethics

Use the attack samples **only** against the bundled demo API, or against systems
you own or are explicitly authorised to test. Never point them at systems you
do not own.
