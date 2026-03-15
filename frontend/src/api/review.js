/**
 * API client for the code review backend.
 */

const REVIEW_API_URL = 'http://localhost:8000/review-code'

/**
 * Request an AI code review from the backend.
 * @param {string} code - Source code to review
 * @param {string} [language] - Optional language hint (e.g. "Python", "JavaScript")
 * @returns {Promise<{ review: string }>}
 * @throws {Error} On network or server error
 */
export async function submitCodeForReview(code, language = null) {
  const body = { code }
  if (language && language !== 'auto') body.language = language

  const response = await fetch(REVIEW_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  })

  if (!response.ok) {
    const text = await response.text()
    let message = text || `Request failed: ${response.status}`
    try {
      const json = JSON.parse(text)
      if (json.detail) message = typeof json.detail === 'string' ? json.detail : json.detail[0]?.msg || message
    } catch (_) {}
    throw new Error(message)
  }

  const data = await response.json()
  return data
}
