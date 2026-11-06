# functional-testing-2507215

Functional tests, CI/CD and live deployment for `target.py` (16 functions).

![CI](https://github.com/<mansurulakash19>/functional-testing-2507215/actions/workflows/ci.yml/badge.svg)

**Live site:** https://<functional-testing-2507215>.onrender.com
**Health / deployed SHA:** https://<functional-testing-2507215>.onrender.com/health

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the tests

```bash
pytest --cov=target --cov-branch --cov-report=term-missing
```

Run the site locally: `python -m flask --app app run`

## Project layout

- `target.py` - the 16 functions (not modified)
- `tests/test_target.py` - functional tests (valid, boundary, invalid, wrong type)
- `app.py`, `runner.py` - Flask frontend and the code that calls `target.py`
- `.github/workflows/ci.yml` - test, deploy and smoke-test jobs

## Pipeline

Every push runs the `test` job on Python 3.10, 3.11 and 3.12 (lint, tests, 100% coverage gate,
coverage artifact). On a push to `main` where tests pass, `deploy` calls the Render deploy hook
for that exact commit, then `smoke-test` waits for `/health` to show the new SHA and makes three
live requests. Render auto-deploy is switched off, so failing code never goes live.

## Suspected bugs in target.py

1. `is_adult("abc")` / `is_adult(None)` fail with a raw comparison `TypeError`, not a clear message.
2. `greet(123)` crashes with `AttributeError` (`int` has no `strip`).
3. `find_max` and `average` accept bools and strings (`average([True, False])` is `0.5`).
4. `factorial(2.5)` and `factorial(3.0)` raise a confusing `TypeError` from `range`;
   `factorial(True)` returns `1`.
5. `to_int(3.9)` silently truncates to `3`; `to_int("3.5")` raises `ValueError`.
6. `divide(1, "a")`, `power("a", 2)` and `square_root("4")` have no input validation.
7. `is_leap_year(2000.5)` has no type check and does not reject non-integers.
8. `celsius_to_fahrenheit("20")` fails with a raw `TypeError`.
9. `swap("ab")` accepts a string and returns `("b", "a")`; `swap([1, 2])` returns a tuple.
10. `common_items(5, 6)` returns `4` (bitwise AND) instead of rejecting non-sets.
