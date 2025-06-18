import copy
import random
from concurrent.futures import ProcessPoolExecutor
from itertools import repeat
from main import *


def random_move(state):
    possible_moves = get_possible_moves(state)
    for moves_index in range(len(possible_moves)):
        possible_moves[moves_index] = f"{chr(possible_moves[moves_index][0] + 97)}{possible_moves[moves_index][1]}"
    if possible_moves is None:
        return None
    move = random.choice(possible_moves)
    return move


def make_move(board, move, side):
    move_col = move[0]
    move_row = move[1]
    if side.lower() == "a":
        board[move_row][move_col] = "◼︎"
    else:
        board[move_row][move_col] = "☐"
    return board


def is_sublist(a, b):
    for i in range(len(b) - len(a) + 1):
        if b[i:i + len(a)] == a:
            return True
    return False


def evaluate(board, side):

    def score_evaluate(board, side):
        score = {
            'five': 1000000,  # BBBBB
            'live_four': 10000,  # _BBBB_
            'jump_four': 8000,  # BBB_B/BB_BB
            'dead_four': 5000,  # BBBB_/_BBBB
            'live_three': 1000,  # _BBB_
            'jump_three': 800,  # _BB_B_/B_BB
            'dead_three': 300,  # BBB__
            'live_two': 100,  # _BB_
            'dead_two': 30,  # BB__/__BB
            'single': 5  # B
        }
        if side == 'a':
            x = '◼︎'
        else:
            x = '☐'

        def score_cnt(x, direction):
            inner_score = 0
            if is_sublist([x, x, x, x, x], direction):
                inner_score += score['five']
            elif is_sublist(['', x, x, x, x, ''], direction):
                inner_score += score['live_four']
            elif is_sublist(['', x, x, x, '', x], direction) \
                    or is_sublist(['', x, x, '', x, x], direction) \
                    or is_sublist(['', x, '', x, x, x], direction):
                inner_score += score['jump_four']
            elif is_sublist(['', x, x, x, x], direction) \
                    or is_sublist([x, x, x, x, ''], direction):
                inner_score += score['dead_four']
            elif is_sublist(['', x, x, x, ''], direction):
                inner_score += score['live_three']
            elif is_sublist(['', x, x, '', x, ''], direction) \
                    or is_sublist([x, '', x, x], direction):
                inner_score += score['jump_three']
            elif is_sublist([x, x, x, '', ''], direction) \
                    or is_sublist(['', '', x, x, x], direction):
                inner_score += score['dead_three']
            elif is_sublist(['', x, x, ''], direction):
                inner_score += score['live_two']
            elif is_sublist(['', '', x, x], direction) \
                    or is_sublist([x, x, '', ''], direction):
                inner_score += score['dead_two']
            else:
                inner_score += 5
            return inner_score

        myscore = 0
        for row_num in range(len(board)):
            row = board[row_num]
            for col_num in range(len(row)):
                box = row[col_num]
                # downwards
                down = get_line(board, row_num, col_num, 0, 1)
                myscore += score_cnt(x, down)

                # rightwards
                right = get_line(board, row_num, col_num, 1, 0)
                myscore += score_cnt(x, right)

                # diagonal
                diagonal = get_line(board, row_num, col_num, 1, 1)
                myscore += score_cnt(x, diagonal)
        return myscore

    my_score = score_evaluate(board, side)
    enemy_score = score_evaluate(board, opposite(side))
    return my_score - 1.2*enemy_score


def minimax(board, side, is_maximized, depth):
    if win(board) or depth == 0:
        return evaluate(board, side)
    # player's side
    if is_maximized:
        best_score = float('-inf')
        for move in get_possible_moves(board):
            new_board = make_move(copy.deepcopy(board), move, side)
            score = minimax(new_board, opposite(side), False, depth - 1)
            best_score = max(best_score, score)
        return best_score
    # ai's side
    if not is_maximized:
        best_score = float('inf')
        for move in get_possible_moves(board):
            new_board = make_move(copy.deepcopy(board), move, opposite(side))
            score = minimax(new_board, opposite(side), True, depth - 1)
            best_score = min(best_score, score)
        return best_score


def evaluate_move(move, board, side, depth):
    new_board = make_move(copy.deepcopy(board), move, side)
    score = minimax(new_board, side, False, depth - 1)
    return [move, score]


def get_best_move(board, side, depth):
    best_score = float('-inf')
    best_move = None
    with ProcessPoolExecutor() as executor:
        for val in executor.map(evaluate_move, get_possible_moves(board),
                                repeat(board), repeat(side), repeat(depth)):
            if val[1] > best_score:
                best_score = val[1]
                best_move = val[0]
    if best_move is None:
        raise Exception('No valid move found')
    best_move = f'{chr(best_move[0] + 97)}{best_move[1] + 1}'
    print(best_move)
    return best_move  # string
