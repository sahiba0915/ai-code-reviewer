import { useState } from 'react'
import CodeEditor from './components/CodeEditor'
import ReviewButton from './components/ReviewButton'
import ReviewResult from './components/ReviewResult'
import { submitCodeForReview } from './api/review'
import './App.css'

function App() {
  const [code, setCode] = useState('')
  const [review, setReview] = useState('')
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  async function handleReviewCode() {
    setError(null)
    setReview('')
    setIsLoading(true)

    try {
      const data = await submitCodeForReview(code)
      setReview(data.review ?? '')
    } catch (err) {
      setError(err.message || 'Failed to get review. Is the backend running at http://localhost:8000?')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="app">
      <header className="app-header">
        <h1>AI Code Reviewer</h1>
        <p>Paste your code below and request an AI-powered review.</p>
      </header>

      <section className="app-content">
        <div className="input-section">
          <label htmlFor="code-editor" className="section-title">
            Code Input
          </label>
          <CodeEditor
            value={code}
            onChange={setCode}
            disabled={isLoading}
          />
          <ReviewButton
            onClick={handleReviewCode}
            disabled={isLoading}
            isLoading={isLoading}
          />
        </div>

        <div className="result-section">
          <h2 className="section-title">AI Review Result</h2>
          <ReviewResult
            review={review}
            error={error}
            isLoading={isLoading}
          />
        </div>
      </section>
    </main>
  )
}

export default App
