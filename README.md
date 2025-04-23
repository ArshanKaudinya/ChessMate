# ♟️ ChessMate

**ChessMate** is a real-time chess assistant that watches your moves, evaluates them using Stockfish, and gives emotionally resonant, coach-style feedback — live. After the game, it offers a post-game chat powered by GPT to help you understand your biggest mistakes.

> Currently in active development.

---

## What I’m Building

- A **Tauri + React** desktop app (lightweight, fast, native)
- A **Python FastAPI** backend for evaluation, tagging, and GPT feedback
- A custom **tagging engine** that detects mistakes like:
  - Early queen moves
  - Missed tactics
  - King exposure
  - Wasted tempos
- A clean, low-cost fallback to GPT-4o for nuanced feedback when rules don’t apply

---

## Key Technologies

- **Stockfish**: real-time UCI chess engine analysis
- **FastAPI**: Python backend for FEN evaluation & feedback
- **OpenAI GPT**: post-game chat + fallback commentary
- **Tauri + Vite + React**: native desktop UI
- **Rule-based tagging**: YAML-driven feedback logic
- **Built inside WSL2** for Linux-native development on Windows

---

_ChessMate is being built with care, precision, and long-term vision. Stay tuned._
