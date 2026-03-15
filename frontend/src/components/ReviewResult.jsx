/**
 * ReviewResult – displays the AI review text with basic formatting.
 */
function ReviewResult({ review, error, isLoading }) {
  if (isLoading) {
    return (
      <div className="review-result" aria-live="polite">
        <p className="review-result-placeholder">Loading review...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="review-result review-result--error" role="alert">
        <p className="review-result-error">{error}</p>
      </div>
    )
  }

  if (!review || review.trim() === '') {
    return (
      <div className="review-result">
        <p className="review-result-placeholder">No review yet. Paste code and click Review Code.</p>
      </div>
    )
  }

  return (
    <div className="review-result">
      <pre className="review-result-text">{review}</pre>
    </div>
  )
}

export default ReviewResult
