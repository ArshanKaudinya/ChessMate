import subprocess, shlex
from pathlib import Path

STOCKFISH_BIN = Path.home() / "dev/chessmate/engines/stockfish-bin/stockfish-ubuntu-x86-64-avx2"


def evaluate_fen(fen: str, depth: int = 15) -> dict:
    proc = subprocess.Popen(
        shlex.split(str(STOCKFISH_BIN)),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    cmds = "\n".join([
        "uci",
        "isready",
        f"position fen {fen}",
        f"go depth {depth}",
        "quit"
    ]) + "\n"
    out, err = proc.communicate(cmds, timeout=10)

    best_move, score_cp = None, None
    for line in out.splitlines():
        if line.startswith("bestmove"):
            best_move = line.split()[1]
        if " cp " in line and "score" in line:
            try:
                score_cp = int(line.split(" cp ")[1].split()[0])
            except ValueError:
                pass
    return {"best_move": best_move, "raw": out, "score_cp": score_cp, "error": err or None}

