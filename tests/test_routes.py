"""Integration tests for the REST API routes."""

import json

import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def post(client, endpoint, payload, content_type="application/json"):
    return client.post(
        endpoint,
        data=json.dumps(payload),
        content_type=content_type,
    )


# ---------------------------------------------------------------------------
# /api/add
# ---------------------------------------------------------------------------
class TestAddRoute:
    def test_add_integers(self, client):
        r = post(client, "/api/add", {"a": 3, "b": 5})
        assert r.status_code == 200
        assert r.get_json()["result"] == 8

    def test_add_floats(self, client):
        r = post(client, "/api/add", {"a": 1.5, "b": 2.5})
        assert r.status_code == 200
        assert r.get_json()["result"] == pytest.approx(4.0)

    def test_add_negative(self, client):
        r = post(client, "/api/add", {"a": -10, "b": 3})
        assert r.status_code == 200
        assert r.get_json()["result"] == -7

    def test_add_missing_field(self, client):
        r = post(client, "/api/add", {"a": 5})
        assert r.status_code == 400
        assert "error" in r.get_json()

    def test_add_non_numeric(self, client):
        r = post(client, "/api/add", {"a": "hello", "b": 2})
        assert r.status_code == 422

    def test_add_invalid_json(self, client):
        r = client.post("/api/add", data="not-json", content_type="application/json")
        assert r.status_code == 400


# ---------------------------------------------------------------------------
# /api/subtract
# ---------------------------------------------------------------------------
class TestSubtractRoute:
    def test_subtract_basic(self, client):
        r = post(client, "/api/subtract", {"a": 10, "b": 4})
        assert r.status_code == 200
        assert r.get_json()["result"] == 6

    def test_subtract_missing_field(self, client):
        r = post(client, "/api/subtract", {"b": 4})
        assert r.status_code == 400

    def test_subtract_non_numeric(self, client):
        r = post(client, "/api/subtract", {"a": "x", "b": 1})
        assert r.status_code == 422


# ---------------------------------------------------------------------------
# /api/multiply
# ---------------------------------------------------------------------------
class TestMultiplyRoute:
    def test_multiply_basic(self, client):
        r = post(client, "/api/multiply", {"a": 6, "b": 7})
        assert r.status_code == 200
        assert r.get_json()["result"] == 42

    def test_multiply_by_zero(self, client):
        r = post(client, "/api/multiply", {"a": 999, "b": 0})
        assert r.status_code == 200
        assert r.get_json()["result"] == 0

    def test_multiply_missing_both(self, client):
        r = post(client, "/api/multiply", {})
        assert r.status_code == 400


# ---------------------------------------------------------------------------
# /api/divide
# ---------------------------------------------------------------------------
class TestDivideRoute:
    def test_divide_basic(self, client):
        r = post(client, "/api/divide", {"a": 10, "b": 2})
        assert r.status_code == 200
        assert r.get_json()["result"] == 5.0

    def test_divide_float_result(self, client):
        r = post(client, "/api/divide", {"a": 7, "b": 2})
        assert r.status_code == 200
        assert r.get_json()["result"] == pytest.approx(3.5)

    def test_divide_by_zero(self, client):
        r = post(client, "/api/divide", {"a": 5, "b": 0})
        assert r.status_code == 400
        assert "error" in r.get_json()
        assert "zero" in r.get_json()["error"].lower()

    def test_divide_missing_field(self, client):
        r = post(client, "/api/divide", {"a": 5})
        assert r.status_code == 400

    def test_divide_non_numeric(self, client):
        r = post(client, "/api/divide", {"a": 5, "b": "two"})
        assert r.status_code == 422


# ---------------------------------------------------------------------------
# /api/health
# ---------------------------------------------------------------------------
class TestHealth:
    def test_health_ok(self, client):
        r = client.get("/api/health")
        assert r.status_code == 200
        assert r.get_json()["status"] == "ok"
