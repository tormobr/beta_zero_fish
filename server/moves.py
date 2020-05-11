import multipliers
import time
from copy import deepcopy
import random
from board import Board
import chess

def get_best_move(moves, turn, fen):
    game = chess.Board(fen)
    board = Board(fen.split()[0])
    new_game = deepcopy(game)
    best = rec(board, game, 3, turn, 3, -10000, 10000)[1]

    ret = {"best": {"from": best.uci()[:2], "to": best.uci()[2:]}}
    print(ret)
    return ret


def rec(board, game, depth, turn, og_depth, alpha, beta):
    if depth == 0:
        return get_board_score(game, board)
            
    moves = game.legal_moves
    scores = []
    for m in moves:
        new_game = deepcopy(game)
        new_board = deepcopy(board)
        f, t = m.uci()[:2], m.uci()[2:]
        new_board.move(f, t)
        new_game.push(m)
        if turn == "b":
            new_score = rec(new_board, new_game, depth-1, "w", og_depth, alpha, beta)
            scores.append((new_score, m))
            beta = min(beta, new_score)
            if beta <= alpha:
                print("brakinbg here in black edition")
                break
        else:
            new_score = rec(new_board, new_game, depth-1, "b", og_depth, alpha, beta)
            scores.append((new_score, m))
            alpha = max(alpha, new_score)
            if beta <= alpha:
                print("brakinbg here in white edition")
                break

    if turn == "b":
        if not scores:
            s = 1000
        else:
            s = min(scores, key=lambda x:x[0])
    else:
        if not scores:
            s = -1000
        else:
            s = max(scores, key=lambda x:x[0])
    if depth != og_depth:
        s = s[0] 
    return s
    

     


def get_board_score(game, board):
    score = 0
    for i, row in enumerate(board.grid):
        for j, elem in enumerate(row):
            score += elem
    return score


def get_legal_moves(game):
    return [{"from": m.uci()[:2], "to":m.uci()[2:]} for m in game.legal_moves]

