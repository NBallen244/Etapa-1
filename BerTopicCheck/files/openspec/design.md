## Context

The workspace starts as a blank slate for the calculator application. To meet requirements, we must construct a dual-layer application: a robust Python backend for exact-precision arithmetic and a React frontend for the interactive visual interface. See `proposal.md` for overall motivation.

## Goals / Non-Goals

**Goals:**
- Implement an AST (Abstract Syntax Tree) safe expression parser in Python using the `decimal` library to guarantee exact math evaluation and avoid security flaws of direct `eval()`.
- Define a single backend REST API endpoint `POST /api/v1/evaluate`.
- Build a responsive React/TypeScript frontend containing a grid of keys and double display (expression and result) resembling standard desktop calculators.
- Ensure 100% test coverage of arithmetic operations (including nested parentheses and PEMDAS precedence).

**Non-Goals:**
- Server-side persistent storage of history (history is transient in the UI).
- Support for complex non-arithmetic operations (e.g., trigonometric, integrals, calculus functions).
- User authentication and multi-user sessions.

## Decisions

### Decision 1: Safe Expression Evaluation Strategy
We will implement an explicit math evaluator rather than using Python's raw `eval()`.
- **Selected Approach**: Parse the expression into an Abstract Syntax Tree using Python's `ast` module (via `ast.parse` in `ast.eval_node` mode) and traverse it using a safe visitor pattern that only allows binary operations, unary operations, numbers, and parentheses. All operations will use Python's `decimal.Decimal` objects to prevent standard IEEE-754 float representation issues.
- **Alternatives Considered**: 
  1. *Dijkstra's Shunting-yard Algorithm*: A manual parsing approach. While functional, it requires custom stack operations and tokenization. The Python AST parser is built-in, fully robust, and highly secure when restricted via custom visitor logic.
  2. *Standard Python `eval()`*: Fast to implement, but poses critical remote code execution (RCE) risks if input sanitization is bypassed.

### Decision 2: Responsive Frontend Layout and Styling
- **Selected Approach**: Build a responsive dashboard using CSS Flexbox/Grid with standard Vanilla CSS for maximum flexibility and clean styling without styling overhead.
- **Alternatives Considered**:
  1. *TailwindCSS*: Rejected to follow default project standards (prefer Vanilla CSS unless explicitly requested).
  2. *Component Library (e.g., Material-UI)*: Overhead of heavy third-party bundles is unnecessary for a dedicated single-purpose application.

### Decision 3: Accessibility (a11y) & Keyboard Bindings
- **Selected Approach**: Bind window-level keydown listeners in React. The listener maps keyboard keys directly to calculator action hooks. Standard buttons will use appropriate semantic `<button>` elements with `aria-label` attributes and an `aria-live="polite"` container for live results.
- **Alternatives Considered**: 
  1. *Focus-based listeners on the wrapper*: Leads to a fragile UX if the wrapper loses focus. Window-level listeners ensure keyboard input is captured regardless of click states.

## Risks / Trade-offs

- **[Risk] Remote Code Execution through API Input** -> *Mitigation*: The input string is strictly sanitized to allow only numeric characters (`0-9`), decimal points (`.`), operators (`+`, `-`, `*`, `/`), and parentheses (`(`, `)`). The AST evaluator strictly white-lists node types and raises errors if any invalid AST nodes (e.g., call nodes, variable loads) are present.
- **[Risk] Division by Zero runtime crash** -> *Mitigation*: Intercept division operations in the AST walker and explicitly raise a custom `ZeroDivisionError` which the FastAPI router captures to return a clean 400 Bad Request error.
