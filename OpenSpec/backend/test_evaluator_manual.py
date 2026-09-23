from evaluator import evaluate_expression
from decimal import Decimal

def test_cases():
    test_expressions = [
        ("0.1 + 0.2", Decimal("0.3")),
        ("12.5 + 3 * (4 - 1.5) / 2", Decimal("16.25")),
        ("-5 + 3", Decimal("-2")),
        ("10 / 2", Decimal("5")),
        ("((2 + 3) * 4) - 5", Decimal("15")),
        ("1.00000000000000000001 + 2", Decimal("3.00000000000000000001")),
    ]

    print("Running manual test cases...")
    all_passed = True
    for expr, expected in test_expressions:
        try:
            res = evaluate_expression(expr)
            if res == expected:
                print(f"✓ '{expr}' = {res} (Expected: {expected})")
            else:
                print(f"✗ '{expr}' = {res} (Expected: {expected})")
                all_passed = False
        except Exception as e:
            print(f"✗ '{expr}' raised exception {type(e).__name__}: {e}")
            all_passed = False

    # Error cases
    error_cases = [
        ("10 / 0", ZeroDivisionError),
        ("12 + * 3", ValueError),
        ("import os; os.system('echo hacked')", ValueError),
    ]

    print("\nRunning error cases...")
    for expr, expected_exc in error_cases:
        try:
            evaluate_expression(expr)
            print(f"✗ '{expr}' did not raise expected exception {expected_exc.__name__}")
            all_passed = False
        except Exception as e:
            if isinstance(e, expected_exc):
                print(f"✓ '{expr}' correctly raised {type(e).__name__}: {e}")
            else:
                print(f"✗ '{expr}' raised {type(e).__name__} instead of {expected_exc.__name__}")
                all_passed = False

    if all_passed:
        print("\nAll manual tests passed!")
    else:
        print("\nSome tests failed!")

if __name__ == "__main__":
    test_cases()
