from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from stockfish_interface import evaluate_fen
from tagger import apply_tags, TAG_RULES
from genAI_interface import gemini_fallback
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

class EvalReq(BaseModel):
    fen: str
    depth: int = 15

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        short, long = gemini_fallback(req.fen, eval_drop)

    return {
        "fen": req.fen,
        "best_move": sf["best_move"],
        "score_cp": sf["score_cp"],
        "tags": tags,
        "short": short,
        "long": long
    }