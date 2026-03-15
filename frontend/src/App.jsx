import { useState, useRef } from 'react'
import CodeEditor from './components/CodeEditor'
import ReviewButton from './components/ReviewButton'
import ReviewResult from './components/ReviewResult'
import { submitCodeForReview } from './api/review'
import './App.css'

const LANGUAGE_OPTIONS = [
  { value: 'auto', label: 'Auto-detect' },
  { value: 'Python', label: 'Python' },
  { value: 'JavaScript', label: 'JavaScript' },
  { value: 'TypeScript', label: 'TypeScript' },
  { value: 'Java', label: 'Java' },
  { value: 'Go', label: 'Go' },
  { value: 'Rust', label: 'Rust' },
  { value: 'C/C++', label: 'C/C++' },
  { value: 'C#', label: 'C#' },
  { value: 'Ruby', label: 'Ruby' },
  { value: 'Other', label: 'Other' },
]

const ACCEPT_FILES = '.py,.js,.jsx,.ts,.tsx,.java,.go,.rs,.c,.cpp,.h,.cs,.rb,.php,.swift,.kt'

function App() {
  const [code, setCode] = useState('')
  const [review, setReview] = useState('')
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [language, setLanguage] = useState('auto')
  const fileInputRef = useRef(null)

  async function handleReviewCode() {
    setError(null)
    setReview('')
    setIsLoading(true)

    try {
      const data = await submitCodeForReview(code, language)
      setReview(data.review ?? '')
    } catch (err) {
      setError(err.message || 'Failed to get review. Is the backend running at http://localhost:8000?')
    } finally {
      setIsLoading(false)
    }
  }

  function handleFileChange(e) {
    const file = e.target.files?.[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = () => {
      setCode(String(reader.result ?? ''))
      setError(null)
    }
    reader.readAsText(file)
    e.target.value = ''
  }

  return (
    <main className="app">
      <header className="app-header">
        <h1>AI Code Reviewer</h1>
        <p>Paste code, upload a file, pick a language, and get an AI-powered review.</p>
      </header>

      <section className="app-content">
        <div className="input-section">
          <div className="input-toolbar">
            <label className="section-title">Code Input</label>
            <div className="toolbar-controls">
              <label className="language-label">
                Language
                <select
                  className="language-select"
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  disabled={isLoading}
                  aria-label="Code language"
                >
                  {LANGUAGE_OPTIONS.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                      {opt.label}
                    </option>
                  ))}
                </select>
              </label>
              <input
                ref={fileInputRef}
                type="file"
                accept={ACCEPT_FILES}
                onChange={handleFileChange}
                className="file-input-hidden"
                aria-label="Upload code file"
              />
              <button
                type="button"
                className="upload-button"
                onClick={() => fileInputRef.current?.click()}
                disabled={isLoading}
              >
                Upload file
              </button>
            </div>
          </div>
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
