# About this code

These samples accompany *Defending APIs* (Colin Domoney, Packt, 2024).

They are **illustrative placeholder samples** intended to demonstrate the concepts
discussed in each chapter. They are deliberately compact and are meant as a starting
point for readers to extend and experiment with — they are **not** production-ready
and, in the case of the attack/vulnerable samples, are intentionally insecure.

> Portions of this sample code were generated with AI assistance and reviewed by the
> author. Use them for learning only.

## Layout

- `common/demo_vulnerable_api/` — a small, intentionally vulnerable FastAPI app used
  as a shared target by the attack chapters (5–7) and as the "before" picture that the
  defence chapters (8–12) improve upon.
- `ChapterNN/` — self-contained samples for each chapter, with a per-chapter README.

## Running

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Then follow the README in each chapter folder.

## Safety / ethics

The attack samples are for use **only** against the bundled demo API or systems you
own or are explicitly authorised to test. Never point them at systems you do not own.

## Tests

A small pytest suite in `tests/` verifies both sides of the story: that the demo API
is exploitable (BOLA, forged-admin BFLA, password-less login) and that the Chapter 9
secure API blocks the same attacks (token rejection, ownership checks, role checks,
mass-assignment rejection), plus unit tests for JWT fail-closed behaviour, scope
matching and positive-model validation.

```bash
pip install -r requirements.txt pytest httpx
JWT_SECRET=$(python -c "import secrets;print(secrets.token_hex(32))") pytest -q
```
