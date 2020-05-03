from copy import deepcopy
import random

def get_best_move(moves, turn, board):
    best = random.choice(get_legal_moves(board))
    return {"best": {"from": best["from"], "to": best["to"]}}


def get_legal_moves(board):
    return [{"from": m.uci()[:2], "to":m.uci()[2:]} for m in board.legal_moves]

