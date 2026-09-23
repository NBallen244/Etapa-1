import pytest
from decimal import Decimal
from evaluator import evaluate_expression

def test_basic_arithmetic():
    assert evaluate_expression("5 + 3") == Decimal("8")
    assert evaluate_expression("10 - 4") == Decimal("6")
    assert evaluate_expression("2 * 6") == Decimal("12")
    assert evaluate_expression("15 / 3") == Decimal("5")

def test_decimal_precision():
    # Floating point precision issues should be avoided
    assert evaluate_expression("0.1 + 0.2") == Decimal("0.3")
    assert evaluate_expression("0.3 - 0.2") == Decimal("0.1")
    assert evaluate_expression("0.1 * 0.2") == Decimal("0.02")
    assert evaluate_expression("0.3 / 0.1") == Decimal("3")

def test_pemdas_precedence():
    # Precedence of operators
    assert evaluate_expression("2 + 3 * 4") == Decimal("14")
    assert evaluate_expression("2 * 3 + 4") == Decimal("10")
    assert evaluate_expression("12 / 3 - 1") == Decimal("3")
    assert evaluate_expression("12 - 3 / 3") == Decimal("11")
    assert evaluate_expression("12.5 + 3 * (4 - 1.5) / 2") == Decimal("16.25")

def test_parentheses():
    # Grouping with nested parentheses
    assert evaluate_expression("(2 + 3) * 4") == Decimal("20")
    assert evaluate_expression("2 * (3 + 4)") == Decimal("14")
    assert evaluate_expression("((2 + 3) * 4) - 5") == Decimal("15")
    assert evaluate_expression("5 * (3 + (2 - 1) * 4)") == Decimal("35")

def test_unary_operators():
    # Negative and positive numbers
    assert evaluate_expression("-5 + 3") == Decimal("-2")
    assert evaluate_expression("+5 + 3") == Decimal("8")
    assert evaluate_expression("-(5 + 3)") == Decimal("-8")
    assert evaluate_expression("-5 * -3") == Decimal("15")

def test_division_by_zero():
    with pytest.raises(ZeroDivisionError, match="Division by zero is not allowed."):
        evaluate_expression("10 / 0")

    with pytest.raises(ZeroDivisionError, match="Division by zero is not allowed."):
        evaluate_expression("5 / (2 - 2)")

def test_invalid_characters():
    with pytest.raises(ValueError, match="contains invalid characters"):
        evaluate_expression("10 + x")

    with pytest.raises(ValueError, match="contains invalid characters"):
        evaluate_expression("import os")

    with pytest.raises(ValueError, match="contains invalid characters"):
        evaluate_expression("10 + 2; print(1)")

def test_syntax_errors():
    with pytest.raises(ValueError, match="Syntax error in expression"):
        evaluate_expression("12 + * 3")

    with pytest.raises(ValueError, match="Syntax error in expression"):
        evaluate_expression("(1 + 2")

    with pytest.raises(ValueError, match="Syntax error in expression"):
        evaluate_expression("1 + 2)")

    with pytest.raises(ValueError, match="Expression is empty"):
        evaluate_expression("   ")
