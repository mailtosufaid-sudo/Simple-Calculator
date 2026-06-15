# Calculator App — Architecture & Design Document

## Requirements

| Operation  | Endpoint          | Method | Description                          |
|------------|-------------------|--------|--------------------------------------|
| Add        | `/api/add`        | POST   | Returns sum of two numbers           |
| Subtract   | `/api/subtract`   | POST   | Returns difference of two numbers    |
| Multiply   | `/api/multiply`   | POST   | Returns product of two numbers       |
| Divide     | `/api/divide`     | POST   | Returns quotient; rejects division by zero |

### Edge Cases Handled
- Division by zero → HTTP 400 with descriptive error message
- Non-numeric input → HTTP 422 with validation error
- Missing request fields → HTTP 400 with descriptive error message

---

## Tech Stack

| Layer     | Technology              | Reason                                      |
|-----------|-------------------------|---------------------------------------------|
| Backend   | Python 3.x + Flask      | Lightweight, easy REST setup                |
| Frontend  | Plain HTML5 + Vanilla JS | Zero build step, minimal dependency         |
| Testing   | pytest + pytest-cov     | Standard Python test runner with coverage   |
| Reporting | pytest-html             | Generates self-contained HTML test report   |

---

## Folder Structure

```
calculator-app/
├── ARCHITECTURE.md          ← this document
├── requirements.txt         ← Python dependencies
├── app/
│   ├── __init__.py          ← Flask app factory
│   ├── calculator.py        ← Pure calculator logic (no Flask)
│   └── routes.py            ← REST endpoints
├── static/
│   └── index.html           ← Single-page frontend
└── tests/
    ├── __init__.py
    ├── test_calculator.py   ← Unit tests for pure logic
    └── test_routes.py       ← Integration tests for REST endpoints
```

---

## REST API Contract

### Request body (all endpoints)
```json
{ "a": <number>, "b": <number> }
```

### Success response — HTTP 200
```json
{ "result": <number> }
```

### Error response — HTTP 400 / 422
```json
{ "error": "<description>" }
```

---

## Data Flow

```
Browser (index.html)
  │  fetch POST /api/<op>  { a, b }
  ▼
Flask Router (routes.py)
  │  parse + validate JSON
  ▼
Calculator Module (calculator.py)
  │  pure functions: add / subtract / multiply / divide
  ▼
JSON response  →  Browser renders result
```

---

## Test Strategy

- **Unit tests** (`test_calculator.py`): test each pure function in isolation, including edge cases.
- **Integration tests** (`test_routes.py`): test HTTP layer using Flask test client — valid inputs, missing fields, non-numeric input, divide-by-zero.
- **Coverage target**: ≥ 95 % line coverage.
- **Report**: `pytest --html=tests/report.html --cov=app --cov-report=html`
