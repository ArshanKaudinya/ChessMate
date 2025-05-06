export function extractFEN(): string | null {
    const boardEl =
      document.querySelector('chess-board') ||
      document.querySelector('cg-helper')
    return boardEl?.getAttribute('data-fen') || null
}
  
export function startFENObserver(onChange: (fen: string) => void) {
    let lastFEN: string | null = null

    const observer = new MutationObserver(() => {
    const fen = extractFEN()
    if (fen && fen !== lastFEN) {
        lastFEN = fen
        onChange(fen)          
        }
    })

    observer.observe(document.body, { childList: true, subtree: true })
    console.log('♟️ FEN observer running')
}
  