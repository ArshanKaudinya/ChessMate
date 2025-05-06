import { useEffect, useState } from 'react'
import { getFeedbackForFEN } from '../api/evaluate'

export default function FeedbackBox() {
  const [fen, setFen] = useState('')
  const [shortMsg, setShortMsg] = useState('')
  const [longMsg, setLongMsg] = useState('')
  const [loading, setLoading] = useState(false)

  const handleEvaluate = async (incomingFen?: string) => {
    const activeFEN = incomingFen || fen
    if (!activeFEN.trim()) return
    setLoading(true)

    try {
      const data = await getFeedbackForFEN(activeFEN)
      setShortMsg(data.short)
      setLongMsg(data.long)
      setFen(activeFEN)
    } catch {
      setShortMsg('Error')
      setLongMsg('Could not fetch feedback.')
    } finally {
      setLoading(false)
    }
  }

  // 🔁 Attach live FEN listener from MutationObserver
  useEffect(() => {
    const listener = (e: any) => {
      const newFEN = e.detail
      if (typeof newFEN === 'string') handleEvaluate(newFEN)
    }

    window.addEventListener('fenUpdated', listener)
    return () => window.removeEventListener('fenUpdated', listener)
  }, [])

  return (
    <div className="feedback-box">
      <input
        type="text"
        className="fen-input"
        placeholder="Paste a FEN string..."
        value={fen}
        onChange={(e) => setFen(e.target.value)}
      />
      <button onClick={() => handleEvaluate()} disabled={loading}>
        {loading ? 'Evaluating...' : 'Evaluate'}
      </button>

      {(shortMsg || longMsg) && (
        <div className="feedback-output">
          <p><strong>{shortMsg}</strong></p>
          <p>{longMsg}</p>
        </div>
      )}
    </div>
  )
}
