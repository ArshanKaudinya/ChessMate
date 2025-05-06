import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-pro")

def gemini_fallback(fen: str, eval_drop: int) -> tuple[str, str]:
    prompt = f"""
                You are a world-class chess coach helping a serious player reflect on their most recent move.

                Your job is to provide clear, accurate, and actionable feedback based on the FEN and evaluation swing.

                FEN: {fen}
                Centipawn swing: {eval_drop}

                Guidelines:
                - Be honest, informative, and concise.
                - You may praise when deserved — but only for truly sound or instructive play.
                - Avoid emotional overreactions, sarcasm, or vague positivity.
                - Use confident, coach-style phrasing — direct, but supportive.
                - Prefer strong, concrete insights over generic or obvious statements.

                Output:
                1. A short one-liner (up to 25 words) that captures the quality or problem with the move. This should feel like a smart coach speaking aloud.
                2. A 1–2 sentence explanation of how the move affected the position and why the evaluation shifted.

                Format your output exactly like:
                <coach-style one-liner>
                <concise technical explanation>
                """
    try:
        rsp = model.generate_content(prompt)
        text = rsp.text.strip()
        lines = text.split("\n", 1)
        return lines[0].strip(), lines[1].strip() if len(lines) > 1 else ""
    except Exception as e:
        return "No feedback available.", f"Gemini error: {e}"

