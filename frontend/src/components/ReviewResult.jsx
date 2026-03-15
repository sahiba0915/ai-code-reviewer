/**
 * ReviewResult – chat-style stream of assistant messages.
 */
function ReviewResult({ review, error, isLoading }) {
  const hasReview = Boolean(review && review.trim() !== '')

  return (
    <div className="chat-thread" aria-live="polite">
      {!hasReview && !error && !isLoading && (
        <div className="chat-message chat-message--system">
          <div className="chat-avatar chat-avatar--system">AI</div>
          <div className="chat-bubble">
            <p className="chat-text">
              Paste some code on the left and click <strong>Review Code</strong> to start a new conversation.
            </p>
          </div>
        </div>
      )}

      {isLoading && (
        <div className="chat-message chat-message--assistant chat-message--loading">
          <div className="chat-avatar">AI</div>
          <div className="chat-bubble">
            <p className="chat-text">
              Thinking about your code
              <span className="chat-typing-dots">
                <span />
                <span />
                <span />
              </span>
            </p>
          </div>
        </div>
      )}

      {error && (
        <div className="chat-message chat-message--assistant chat-message--error" role="alert">
          <div className="chat-avatar">!</div>
          <div className="chat-bubble">
            <p className="chat-text chat-text--error">{error}</p>
          </div>
        </div>
      )}

      {hasReview && !isLoading && !error && (
        <div className="chat-message chat-message--assistant">
          <div className="chat-avatar">AI</div>
          <div className="chat-bubble">
            <pre className="chat-text chat-text--mono">{review}</pre>
          </div>
        </div>
      )}
    </div>
  )
}

export default ReviewResult
