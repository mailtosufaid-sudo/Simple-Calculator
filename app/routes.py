from flask import Blueprint, jsonify, request

from .calculator import add, divide, multiply, subtract

bp = Blueprint("calculator", __name__, url_prefix="/api")


def _parse_operands():
    """Extract and validate 'a' and 'b' from the JSON request body."""
    data = request.get_json(silent=True)
    if data is None:
        return None, None, (jsonify({"error": "Request body must be valid JSON."}), 400)

    missing = [field for field in ("a", "b") if field not in data]
    if missing:
        return None, None, (
            jsonify({"error": f"Missing required field(s): {', '.join(missing)}."}),
            400,
        )

    a, b = data["a"], data["b"]
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        return None, None, (
            jsonify({"error": "Fields 'a' and 'b' must be numbers."}),
            422,
        )

    return float(a), float(b), None


@bp.route("/add", methods=["POST"])
def route_add():
    a, b, err = _parse_operands()
    if err:
        return err
    return jsonify({"result": add(a, b)})


@bp.route("/subtract", methods=["POST"])
def route_subtract():
    a, b, err = _parse_operands()
    if err:
        return err
    return jsonify({"result": subtract(a, b)})


@bp.route("/multiply", methods=["POST"])
def route_multiply():
    a, b, err = _parse_operands()
    if err:
        return err
    return jsonify({"result": multiply(a, b)})


@bp.route("/divide", methods=["POST"])
def route_divide():
    a, b, err = _parse_operands()
    if err:
        return err
    try:
        return jsonify({"result": divide(a, b)})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@bp.route("/health")
def health():
    return jsonify({"status": "ok"})
