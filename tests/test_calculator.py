"""Unit tests for the pure calculator logic in app/calculator.py."""

import pytest

from app.calculator import add, divide, multiply, subtract


class TestAdd:
    def test_positive_numbers(self):
        assert add(3, 5) == 8

    def test_negative_numbers(self):
        assert add(-4, -6) == -10

    def test_mixed_sign(self):
        assert add(-3, 7) == 4

    def test_floats(self):
        assert add(1.1, 2.2) == pytest.approx(3.3)

    def test_zero(self):
        assert add(0, 0) == 0

    def test_large_numbers(self):
        assert add(1_000_000, 2_000_000) == 3_000_000


class TestSubtract:
    def test_positive_result(self):
        assert subtract(10, 4) == 6

    def test_negative_result(self):
        assert subtract(4, 10) == -6

    def test_zero_result(self):
        assert subtract(5, 5) == 0

    def test_floats(self):
        assert subtract(3.5, 1.2) == pytest.approx(2.3)

    def test_negative_operands(self):
        assert subtract(-3, -7) == 4


class TestMultiply:
    def test_positive_numbers(self):
        assert multiply(3, 4) == 12

    def test_multiply_by_zero(self):
        assert multiply(99, 0) == 0

    def test_negative_times_positive(self):
        assert multiply(-5, 4) == -20

    def test_negative_times_negative(self):
        assert multiply(-3, -3) == 9

    def test_floats(self):
        assert multiply(2.5, 4.0) == pytest.approx(10.0)

    def test_identity(self):
        assert multiply(7, 1) == 7


class TestDivide:
    def test_exact_division(self):
        assert divide(10, 2) == 5.0

    def test_float_result(self):
        assert divide(7, 2) == pytest.approx(3.5)

    def test_negative_dividend(self):
        assert divide(-9, 3) == -3.0

    def test_negative_divisor(self):
        assert divide(9, -3) == -3.0

    def test_both_negative(self):
        assert divide(-8, -4) == 2.0

    def test_divide_by_zero_raises(self):
        with pytest.raises(ValueError, match="Division by zero"):
            divide(5, 0)

    def test_divide_by_zero_float(self):
        with pytest.raises(ValueError):
            divide(1.0, 0.0)

    def test_zero_dividend(self):
        assert divide(0, 5) == 0.0
