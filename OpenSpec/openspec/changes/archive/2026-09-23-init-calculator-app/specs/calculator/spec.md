## Purpose

Provides a fully responsive mathematical calculator application that parses and evaluates chained arithmetic expressions with exact decimal precision according to PEMDAS rules and supports full keyboard and screen reader accessibility.

## ADDED Requirements

### Requirement: API Mathematical Expression Evaluation
The system SHALL expose a JSON-based REST API endpoint at `POST /api/v1/evaluate` that parses, validates, and evaluates a given mathematical expression string. The system SHALL return the final evaluated numeric value using high-precision decimal representation to prevent standard float rounding errors, adhering strictly to standard PEMDAS operations.

#### Scenario: Successful Evaluation of Chained Expression
- **WHEN** a client sends a `POST` request to `/api/v1/evaluate` with the payload `{"expression": "12.5 + 3 * (4 - 1.5) / 2"}`
- **THEN** the system SHALL return a status code of 200 with JSON payload containing the exact result `16.25`

#### Scenario: Error Evaluation for Division by Zero
- **WHEN** a client sends a `POST` request to `/api/v1/evaluate` with the payload `{"expression": "10 / 0"}`
- **THEN** the system SHALL return a status code of 400 with a descriptive error JSON payload indicating division by zero is not allowed

#### Scenario: Error Evaluation for Invalid Operator Sequences
- **WHEN** a client sends a `POST` request to `/api/v1/evaluate` with the payload `{"expression": "12 + * 3"}`
- **THEN** the system SHALL return a status code of 400 with a descriptive error JSON payload indicating a syntax or operator mismatch error

### Requirement: Desktop Calculator User Interface Layout
The frontend client SHALL render a responsive layout resembling a physical desktop calculator that fits mobile, tablet, and desktop viewports seamlessly. This UI SHALL include a clear display area showing both the full current input expression and the live or final result, and a grid of interactive buttons for numbers `0-9`, decimal point `.`, parentheses `(`, `)`, basic operators `+`, `-`, `*`, `/`, clear `C`, backspace, and evaluation `=`.

#### Scenario: Responsive Component Layout Adjusts to Viewport
- **WHEN** the user views the calculator app on a mobile device of width 375px
- **THEN** the layout SHALL fit the screen entirely without horizontal scrollbars, wrapping text, or clipped buttons

### Requirement: Keyboard and Pointer Event Handling
The frontend client SHALL support mouse clicks / touch taps on all on-screen buttons, and integrate with the user's keyboard. Pressing number keys, standard operators (`+`, `-`, `*`, `/`), parentheses, `Enter` or `=` for evaluate, `Backspace` for clear/delete, and `Escape` for reset SHALL trigger the corresponding calculator inputs and calculation requests.

#### Scenario: Mouse Click Appends Operator and Updates Input State
- **WHEN** the user clicks the "5" button, then the "+" button, then the "3" button
- **THEN** the UI expression display SHALL show "5+3"

#### Scenario: Keyboard Input Triggers Evaluation
- **WHEN** the user types "5+3" on their keyboard and presses the "Enter" key
- **THEN** the client SHALL send the expression to the API and render the result returned by the backend

### Requirement: Accessibility and Screen Reader Compatibility
The frontend client SHALL incorporate standard accessibility (a11y) guidelines, including proper semantic elements or `role="button"`, `aria-label` attributes on every interactive element, explicit active/focus states, and an `aria-live` region for the result and expression displays so screen readers can announce changes dynamically.

#### Scenario: Screen Reader Announces Evaluation Results
- **WHEN** the user triggers an evaluation and a new result is displayed
- **THEN** the `aria-live` region of the result display SHALL be updated with the result, causing the screen reader to announce it
