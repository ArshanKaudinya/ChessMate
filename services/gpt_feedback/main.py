from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from stockfish_interface import evaluate_fen
from tagger import apply_tags, TAG_RULES
import openai, os, functools

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
GPT_CACHE: dict[str, tuple[str, str]] = {}   # tag_id -> (short,long)

class EvalReq(BaseModel):
    fen: str
    depth: int = 15

def gpt_fallback(fen, eval_drop):
    prompt = (
      f"FEN: {fen}\n"
      f"Centipawn swing: {eval_drop}\n"
      "Give a short coach quip (<10 words) then a 2-sentence explanation."
    )
    rsp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=80,
    )
    lines = rsp.choices[0].message.content.split("\n", 1)
    short = lines[0].strip()
    long = lines[1].strip() if len(lines) > 1 else ""
    return short, long

@app.post("/evaluate")
def evaluate(req: EvalReq):
    sf = evaluate_fen(req.fen, req.depth)
    if sf["error"]:
        raise HTTPException(500, sf["error"])

    eval_drop = sf["score_cp"] if sf["score_cp"] is not None else 0
    tags = apply_tags(req.fen, eval_drop, sf["best_move"])
    if tags:
        tag_id = tags[0]
        meta = next(r for r in TAG_RULES if r["id"] == tag_id)
        short, long = meta["short"], meta["long"]
    else:
        # fire GPT only if swing > 50 cp to save cost
        if abs(eval_drop) > 50:
            short, long = GPT_CACHE.get(req.fen) or gpt_fallback(req.fen, eval_drop)
            GPT_CACHE[req.fen] = (short, long)
        else:
            short, long = "Solid move.", "No significant change."

    return {
        "fen": req.fen,
        "best_move": sf["best_move"],
        "score_cp": sf["score_cp"],
        "tags": tags,
        "short": short,
        "long": long
    }

