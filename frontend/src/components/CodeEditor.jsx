/**
 * CodeEditor – large textarea for pasting code to review.
 */
function CodeEditor({ value, onChange, placeholder = 'Paste your code here...', disabled = false }) {
  return (
    <textarea
      id="code-editor"
      className="code-editor"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      rows={16}
      disabled={disabled}
      aria-label="Code input"
    />
  )
}

export default CodeEditor
