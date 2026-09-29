## 1. Backend Setup & Parser Engine

- [x] 1.1 Create the backend project structure (e.g., under a `backend` directory) and verify that a basic Python script can run and output version info.
- [x] 1.2 Implement the safe mathematical expression parser using Python's standard `ast` module and `decimal.Decimal` class, verifying that it correctly respects PEMDAS order of operations and handles arbitrary decimal precision.
- [x] 1.3 Implement comprehensive unit tests using `pytest` covering chained expressions, precedence, nested parentheses, and edge cases, verifying that all tests run and pass.

## 2. FastAPI Web Server & API Endpoint

- [x] 2.1 Set up the FastAPI application and configure the `POST /api/v1/evaluate` route, verifying that it correctly parses incoming JSON payload, calls the calculator parser, and returns the accurate evaluated result.
- [x] 2.2 Add CORS middleware configuration to the FastAPI application and robust exception handlers for syntax errors or divisions by zero, verifying with test requests that API returns clean, descriptive JSON errors with status 400.

## 3. Frontend Client Setup & Components

- [x] 3.1 Initialize the React and TypeScript frontend client using Vite, verifying that the project compiles and starts a development server.
- [x] 3.2 Implement the visual desktop calculator layout using semantic HTML5 and Vanilla CSS with a grid for keys and dual displays for current input and live/final result, verifying the layout adapts responsively to mobile, tablet, and desktop viewports.
- [x] 3.3 Add screen reader accessibility properties, including proper `aria-label` attributes on every button and an `aria-live="polite"` region on the result displays, verifying the attributes are present in the DOM.

## 4. Interactive Logic & End-to-End Integration

- [x] 4.1 Implement React state hooks to track the calculator's current expression string and visual state, verifying that click events on the on-screen buttons append numbers or operators to the input display.
- [x] 4.2 Set up window-level keyboard event listeners in React to bind typing of numbers, standard operators, parentheses, backspace, reset (Escape), and evaluate (Enter) to calculator actions, verifying typing triggers appropriate updates.
- [x] 4.3 Add backend API invocation on submission using standard `fetch` API, rendering the evaluated result on the screen or showing the error returned by the backend, verifying that end-to-end mathematical evaluation succeeds.
