from copy import deepcopy
import random

def is_own(x, y, newx, newy, board):
    b = board.grid[y][x] < 0 and board.grid[newy][newx] < 0
    w = board.grid[y][x] > 0 and board.grid[newy][newx] > 0
    return (b or w)


def moves_knight(x, y, board):
    moves = []
    ms = [(1,2), (1,-2),(-1, 2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]
    for m in ms:
        newx = x +m[0]
        newy = y +m[1]
        if out_of_bounds(newx, newy):
            continue
        if not in_check(x, y, newx, newy, board):
                if board.grid[y][x] != 0:
                    if not is_own(x, y, newx, newy, board):
                        moves.append({"from": (x, y), "to": (newx, newy), "piece": "knight"})
                else:
                    moves.append({"from": (x, y), "to": (newx, newy), "piece": "knight"})
    return moves

def moves_bish(x, y, board):
    moves = []
    dirs = [(1,1), (-1,-1), (-1, 1), (1, -1)]
    for d in dirs:
        newx = x + d[0]
        newy = y + d[1]
        while not out_of_bounds(newx, newy):
            if in_check(x, y, newx, newy, board):
                newx += d[0]
                newy += d[1]
                continue
            if board.grid[newy][newx] == 0:
                moves.append({"from": (x, y), "to": (newx, newy), "piece": "bish"})
            elif is_own(x, y, newx, newy, board):
                break
            else:
                moves.append({"from": (x, y), "to": (newx, newy), "piece": "bish"})
                break
            newx += d[0]
            newy += d[1]
    return moves

def moves_rook(x, y, board):
    print("calling rook function")
    moves = []
    dirs = [(1,0), (0, 1), (-1 ,0), (0, -1)]
    for d in dirs:
        newx = x + d[0]
        newy = y + d[1]
        while not out_of_bounds(newx, newy):
            print("current check for rook: ", newx, newy)
            if in_check(x, y, newx, newy, board):
                newx += d[0]
                newy += d[1]
                continue
            if board.grid[newy][newx] == 0:
                moves.append({"from": (x, y), "to": (newx, newy), "piece": "rook"})
            elif is_own(x, y, newx, newy, board):
                print("hit own.. breaking")
                break
            else:
                moves.append({"from": (x, y), "to": (newx, newy), "piece": "rook"})
                print("capture break")
                break
            newx += d[0]
            newy += d[1]
        print("out of bounds with", newx, newy)
    return moves

def moves_queen(x, y, board):
    moves = []
    moves += moves_rook(x, y, board)
    moves += moves_bish(x, y, board)
    return moves

def moves_king(x, y, board):
    moves = []
    dirs = [(1,0), (0, 1), (-1 ,0), (0, -1), (-1, 1), (1, -1), (-1, -1), (1,1)]
    for d in dirs:
        newx = x + d[0]
        newy = y + d[1]
        if out_of_bounds(newx, newy):
            continue
        if in_check(x, y, newx, newy, board):
            continue
        if board.grid[newy][newx] == 0 or not is_own(x, y, newx, newy, board):
            moves.append({"from": (x, y), "to": (newx, newy), "piece": "king"})
    return moves

def moves_pawn(x, y, board):
    print("move_pawn function cal", x, y)
    moves = []
    dirs = [(0,1), (0,2), (1,1), (-1,1)]
    if board.grid[y][x] == 1:
        dirs = [(x, y*-1) for x,y in dirs]
    
    for d in dirs:
        newx = x + d[0]
        newy = y + d[1]
        if out_of_bounds(newx, newy):
            print("our of bounds")
            continue
        if in_check(x, y, newx, newy, board):
            continue
        if d[0] != 0 and (board.grid[newy][newx] == 0 or is_own(x, y, newx, newy, board)):
            print("striking nothing on: ", x, y)
            continue
        if d[0] == 0 and board.grid[newy][newx] != 0:
            continue

        if abs(d[1]) == 2:
            if y != 1 and y != 6:
                continue
            print("THIOS SHIT HAPPENS DOUBLE MOVE")
            if board.grid[y + dirs[0][1]][x] != 0 or y not in [1, 6]:
                continue
        moves.append({"from": (x, y), "to": (newx, newy), "piece": "pawn"})

    return moves

move_functions = {
    "1": moves_pawn,
    "3": moves_knight,
    "4": moves_bish,
    "5": moves_rook,
    "9": moves_queen,
    "100": moves_king
}

def get_best_move(moves, turn, board):
    #ms = legal_moves(board, turn)
    #print(ms)
    #ret = random.choice(ms)
    #fromm = board.index_to_letter(ret["from"][0], ret["from"][1])
    #to = board.index_to_letter(ret["to"][0], ret["to"][1])
    #res = {"best": {"from": fromm, "to": to}}
    #print(res, ret["piece"])
    #return res
    
    index = 0 
    if turn == "notb":
        move = random.choice(moves)
        board.move(move["from"], move["to"])
        return {"best":move["san"]}
    best = [0,0]
    for i, move in enumerate(moves):
        x, y = board.letter_to_index(move["to"])
        current = board.grid[y][x]
        if turn == "w" and current < best[0]:
            best = [current, i]
        elif turn == "b" and current > best[0]:
            best = [current, i]

    move = moves[best[1]]
    if best[0] == 0:
        move = random.choice(moves)
    board.move(move["from"], move["to"])
    print(move["san"])
    return {'best': move["san"]}

def legal_moves(board, turn):
    moves = []
    for y, row in enumerate(board.grid):
        for x, elem in enumerate(row):
            if (elem == -100 and turn == "b") or (elem == 100 and turn =="w"):
                #print(x)
                moves += move_functions[str(abs(elem))](x, y, board)
            else:
                pass
                #print("turn: ", turn, "elem", elem)
    return moves



def out_of_bounds(x, y):
    if x < 0 or x > 7:
        return True
    if y < 0 or y > 7:
        return True
    return False
    

def in_check(x, y, newx, newy, board):
    tmp_grid = deepcopy(board.grid)
    tmp_grid[newy][newx] = board.grid[y][x]
    tmp_grid[y][x] = 0
    c = 100
    king_loc = None

    if board.grid[y][x] < 0:
        c = -100

    for i, row in enumerate(tmp_grid):
        for j, elem in enumerate(row):
            if elem == c:
                king_loc = (j, i)
    threats = {(1,0): [5, 9],   # straight
               (-1, 0): [5, 9],
               (0, 1): [5, 9],
               (0, -1): [5, 9],
               # diagonal
               (1, 1): [4, 9],
               (-1, 1): [4, 9],
               (1, -1): [4, 9],
               (-1, -1): [4, 9]}
    for d, value in threats.items():
        tmp_x = newx + d[0]
        tmp_y= newx + d[1]
        while not out_of_bounds(tmp_x, tmp_y) and not is_own(newx, newy, tmp_x, tmp_y, board):
            if tmp_grid[tmp_y][tmp_x] in value:
                return True

            tmp_x += d[0]
            tmp_y += d[1]

    return False

    
