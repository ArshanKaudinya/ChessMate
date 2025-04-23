import yaml, re, pathlib
TAG_RULES = yaml.safe_load(
    pathlib.Path(__file__).with_name("tags.yml").read_text()
)

def _get_ctx(fen: str, score_drop: int, best_move: str) -> dict:
    fields = fen.split()
    ply = int(fields[5]) * 2 + (0 if fields[1] == "w" else 1)
    moved_piece = fields[4][-1] if best_move else ""
    moved_file = best_move[0] if best_move else ""
    return {
        "eval_drop": abs(score_drop),
        "ply": ply,
        "piece_moved": moved_piece.upper(),
        "moved_pawn_file": moved_file,
        "castled": "K" in fields[2] or "k" in fields[2],
    }

def apply_tags(fen: str, score_drop: int, best_move: str):
    ctx = _get_ctx(fen, score_drop, best_move)
    tags = []
    for rule in TAG_RULES:
        if eval(rule["when"], {}, ctx):
            tags.append(rule["id"])
    return tags
