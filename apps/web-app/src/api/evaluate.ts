const API_URL = import.meta.env.VITE_API_URL

export async function getFeedbackForFEN(fen: string) {
  const res = await fetch(`${API_URL}/evaluate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ fen }),
  })

  if (!res.ok) throw new Error('Evaluation failed')

  return res.json() as Promise<{
    short: string
    long: string
    best_move: string
    score_cp: number
    tags: string[]
  }>
}
