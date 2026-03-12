import { useState } from 'react'
import './App.css'

function App() {
  // Local state to hold the pasted source code and the review result.
  const [code, setCode] = useState('')
  const [reviewResult, setReviewResult] = useState('')

  return (
    <main className="app">
      <header className="app-header">
        <h1>AI Code Reviewer</h1>
        <p>Paste your code below and request an AI-powered review.</p>
      </header>

      <section className="app-content">
        <div className="input-section">
          <label htmlFor="code-input" className="section-title">
            Code
          </label>
          <textarea
            id="code-input"
            className="code-textarea"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="Paste your code here..."
            rows={14}
          />
          <button
            type="button"
            className="review-button"
            onClick={() => {
              // Integration with the backend will be implemented later.
              setReviewResult('Review will appear here once the backend is connected.')
            }}
          >
            Review
          </button>
        </div>

        <div className="result-section">
          <h2 className="section-title">Review Result</h2>
          <div className="result-box">
            {reviewResult || 'No review yet.'}
          </div>
        </div>
      </section>
    </main>
  )
}

export default App
