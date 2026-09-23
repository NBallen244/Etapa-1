import { useState, useEffect, useCallback } from 'react'

function App() {
  const [expression, setExpression] = useState<string>('')
  const [result, setResult] = useState<string>('')
  const [error, setError] = useState<string>('')
  const [loading, setLoading] = useState<boolean>(false)

  const handleAppend = useCallback((val: string) => {
    setError('')
    setExpression((prev) => prev + val)
  }, [])

  const handleClear = useCallback(() => {
    setExpression('')
    setResult('')
    setError('')
  }, [])

  const handleBackspace = useCallback(() => {
    setError('')
    setExpression((prev) => prev.slice(0, -1))
  }, [])

  const handleEvaluate = useCallback(async () => {
    const trimmed = expression.trim()
    if (!trimmed) return

    setLoading(true)
    setError('')
    try {
      const response = await fetch('/api/v1/evaluate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ expression: trimmed }),
      })

      const data = await response.json()
      if (response.ok) {
        setResult(String(data.result))
      } else {
        setError(data.detail || 'An error occurred during evaluation')
        setResult('')
      }
    } catch (err) {
      setError('Failed to connect to the backend server.')
      setResult('')
    } finally {
      setLoading(false)
    }
  }, [expression])

  // Bind global keyboard listeners
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Do not intercept if focused on inputs/textareas (though none are currently planned)
      const activeElement = document.activeElement
      if (
        activeElement &&
        (activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA')
      ) {
        return
      }

      const key = e.key
      if (/[0-9]/.test(key)) {
        handleAppend(key)
      } else if (key === '.') {
        handleAppend('.')
      } else if (['+', '-', '*', '/'].includes(key)) {
        handleAppend(key)
      } else if (key === '(' || key === ')') {
        handleAppend(key)
      } else if (key === 'Backspace') {
        handleBackspace()
      } else if (key === 'Escape') {
        handleClear()
      } else if (key === 'Enter' || key === '=') {
        e.preventDefault()
        handleEvaluate()
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => {
      window.removeEventListener('keydown', handleKeyDown)
    }
  }, [handleAppend, handleBackspace, handleClear, handleEvaluate])

  return (
    <div className="calculator-app">
      <main className="calculator">
        <h1 className="title">Web Calculator</h1>

        {/* Accessible screen reader announcement region */}
        <div
          className="sr-only"
          aria-live="polite"
          style={{
            position: 'absolute',
            width: '1px',
            height: '1px',
            padding: 0,
            margin: '-1px',
            overflow: 'hidden',
            clip: 'rect(0, 0, 0, 0)',
            border: 0,
          }}
        >
          {error ? `Error: ${error}` : result ? `Result: ${result}` : `Current Expression: ${expression || 'empty'}`}
        </div>

        <section className="display" aria-label="Calculator screen">
          <div className="expression-area" aria-hidden="true">
            {expression || '\u00A0'}
          </div>
          <div
            className={`result-area ${error ? 'error' : ''}`}
            aria-live="polite"
            role="status"
          >
            {loading ? '...' : error ? error : result || '0'}
          </div>
        </section>

        <section className="grid" aria-label="Calculator keyboard">
          <button
            type="button"
            className="calc-btn special"
            onClick={() => handleAppend('(')}
            aria-label="Open parenthesis"
          >
            (
          </button>
          <button
            type="button"
            className="calc-btn special"
            onClick={() => handleAppend(')')}
            aria-label="Close parenthesis"
          >
            )
          </button>
          <button
            type="button"
            className="calc-btn special"
            onClick={handleClear}
            aria-label="Clear all inputs"
          >
            C
          </button>
          <button
            type="button"
            className="calc-btn special"
            onClick={handleBackspace}
            aria-label="Delete last character"
          >
            ⌫
          </button>

          <button
            type="button"
            className="calc-btn number"
            onClick={() => handleAppend('7')}
            aria-label="Number 7"
          >
            7
          </button>
          <button
            type="button"
            className="calc-btn number"
            onClick={() => handleAppend('8')}
            aria-label="Number 8"
          >
            8
          </button>
          <button
            type="button"
            className="calc-btn number"
            onClick={() => handleAppend('9')}
            aria-label="Number 9"
          >
            9
          </button>
          <button
            type="button"
            className="calc-btn operator"
            onClick={() => handleAppend('/')}
            aria-label="Divide"
          >
            /
          </button>

          <button
            type="button"
            className="calc-btn number"
            onClick={() => handleAppend('4')}
            aria-label="Number 4"
          >
            4
          </button>
          <button
            type="button"
            className="calc-btn number"
            onClick={() => handleAppend('5')}
            aria-label="Number 5"
          >
            5
          </button>
          <button
            type="button"
            className="calc-btn number"
            onClick={() => handleAppend('6')}
            aria-label="Number 6"
          >
            6
          </button>
          <button
            type="button"
            className="calc-btn operator"
            onClick={() => handleAppend('*')}
            aria-label="Multiply"
          >
            *
          </button>

          <button
            type="button"
            className="calc-btn number"
            onClick={() => handleAppend('1')}
            aria-label="Number 1"
          >
            1
          </button>
          <button
            type="button"
            className="calc-btn number"
            onClick={() => handleAppend('2')}
            aria-label="Number 2"
          >
            2
          </button>
          <button
            type="button"
            className="calc-btn number"
            onClick={() => handleAppend('3')}
            aria-label="Number 3"
          >
            3
          </button>
          <button
            type="button"
            className="calc-btn operator"
            onClick={() => handleAppend('-')}
            aria-label="Subtract"
          >
            -
          </button>

          <button
            type="button"
            className="calc-btn number"
            onClick={() => handleAppend('0')}
            aria-label="Number 0"
          >
            0
          </button>
          <button
            type="button"
            className="calc-btn number"
            onClick={() => handleAppend('.')}
            aria-label="Decimal point"
          >
            .
          </button>
          <button
            type="button"
            className="calc-btn equals"
            onClick={handleEvaluate}
            aria-label="Evaluate expression"
          >
            =
          </button>
          <button
            type="button"
            className="calc-btn operator"
            onClick={() => handleAppend('+')}
            aria-label="Add"
          >
            +
          </button>
        </section>
      </main>
      <footer className="keyboard-instructions">
        Supports full keyboard entry.
        <br />
        Enter/Equals (=) to calculate, Backspace (⌫) to delete, Esc to clear.
      </footer>
    </div>
  )
}

export default App
