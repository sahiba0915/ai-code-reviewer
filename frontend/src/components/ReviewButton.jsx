/**
 * ReviewButton – triggers code review. Shows loading state and disables while request runs.
 */
function ReviewButton({ onClick, disabled = false, isLoading = false }) {
  return (
    <button
      type="button"
      className="review-button"
      onClick={onClick}
      disabled={disabled}
      aria-busy={isLoading}
    >
      {isLoading ? 'Reviewing code...' : 'Review Code'}
    </button>
  )
}

export default ReviewButton
