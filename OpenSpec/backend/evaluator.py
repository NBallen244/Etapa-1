import ast
import operator
from decimal import Decimal, InvalidOperation, DivisionByZero

# Supported AST operators mapped to standard functions
SUPPORTED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

class SafeEvaluator(ast.NodeVisitor):
    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            # Convert to string first to avoid floating point precision issues during conversion
            return Decimal(str(node.value))
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    def visit_BinOp(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        op_type = type(node.op)
        if op_type in SUPPORTED_OPERATORS:
            if op_type == ast.Div:
                if right_val == Decimal('0'):
                    raise ZeroDivisionError("Division by zero is not allowed.")
                try:
                    return left_val / right_val
                except (DivisionByZero, InvalidOperation):
                    raise ZeroDivisionError("Division by zero is not allowed.")
            return SUPPORTED_OPERATORS[op_type](left_val, right_val)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    def visit_UnaryOp(self, node):
        operand_val = self.visit(node.operand)
        op_type = type(node.op)
        if op_type in SUPPORTED_OPERATORS:
            return SUPPORTED_OPERATORS[op_type](operand_val)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    def generic_visit(self, node):
        raise ValueError(f"Unsupported syntax construct: {type(node).__name__}")

def evaluate_expression(expression: str) -> Decimal:
    """
    Parses and evaluates a mathematical expression string safely with arbitrary decimal precision.
    Supports basic arithmetic operators (+, -, *, /), nested parentheses, and PEMDAS precedence.
    """
    # 1. Basic sanitization
    expression = expression.strip()
    if not expression:
        raise ValueError("Expression is empty.")

    # 2. Strict character whitelist validation
    allowed_chars = set("0123456789.+-*/() ")
    if not set(expression).issubset(allowed_chars):
        invalid_chars = set(expression) - allowed_chars
        raise ValueError(f"Expression contains invalid characters: {''.join(sorted(invalid_chars))}")

    # 3. Parse AST
    try:
        node = ast.parse(expression, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in expression: {e.msg}")

    # 4. Evaluate AST
    evaluator = SafeEvaluator()
    try:
        result = evaluator.visit(node)
    except ZeroDivisionError:
        raise
    except Exception as e:
        raise ValueError(f"Evaluation error: {str(e)}")

    # Standardize result: remove trailing zeros and normalize formatting
    # e.g., 1.5000 -> 1.5, 10.00 -> 10
    if isinstance(result, Decimal):
        # Normalize removes trailing zeros, but returns in exponential format if very large/small.
        # Let's simplify by normalizing.
        try:
            result = result.normalize()
        except Exception:
            pass
    return result
