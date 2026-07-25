# import copy
import random
# from concurrent.futures import ProcessPoolExecutor
# from itertools import repeat
from main import opposite, get_possible_moves, get_line, win, turns_range

TT = {}  # Cache

score = {
    'five': 100000000,  # BBBBB
    'live_four': 1000000,  # _BBBB_
    'jump_four': 100000,  # BBB_B/BB_BB
    'dead_four': 80000,  # BBBB_/_BBBB
    'live_three': 5000,  # _BBB_
    'jump_three': 3000,  # _BB_B_/B_BB
    'dead_three': 500,  # BBB__
    'live_two': 100,  # _BB_
    'dead_two': 30,  # BB__/__BB
    'single': 5  # B
}


def board_key(board):
    return tuple(tuple(row) for row in board)


def make_move(board, move, side):
    move_col = move[0]
    move_row = move[1]
    if side.lower() == "a":
        board[move_row][move_col] = "◼︎"
    else:
        board[move_row][move_col] = "☐"


def undo_move(board, move):
    move_col = move[0]
    move_row = move[1]
    board[move_row][move_col] = ''


# def is_sublist(a, b):
#     for i in range(len(b) - len(a) + 1):
#         if b[i:i + len(a)] == a:
#             return True
#     return False


def global_patterns_detect(board, side):
    def convert(p, side):
        if (side == "a" and p == "◼︎") or (side == "b" and p == "☐"):
            return 'X'
        elif p == "":
            return '_'
        else:
            return 'O'

    patterns = []
    for row_num in range(len(board)):
        row = board[row_num]
        for col_num in range(len(row)):
            box = row[col_num]
            # downwards
            down = ''.join(convert(p, side) for p in get_line(board, row_num, col_num, 0, 1))
            # rightwards
            right = ''.join(convert(p, side) for p in get_line(board, row_num, col_num, 1, 0))
            # right_down
            right_down = ''.join(convert(p, side) for p in get_line(board, row_num, col_num, 1, 1))
            # right_up
            right_up = ''.join(convert(p, side) for p in get_line(board, row_num, col_num, -1, 1))

            directions = [down, right, right_down, right_up]
            for direction in directions:
                if 'XXXXX' in direction:
                    patterns.append('five')
                elif '_XXXX_' in direction:
                    patterns.append('live_four')
                elif '_XXX_X' in direction \
                        or '_XX_XX' in direction \
                        or '_X_XXX' in direction:
                    patterns.append('jump_four')
                elif '_XXXX' in direction \
                        or 'XXXX_' in direction:
                    patterns.append('dead_four')
                elif '_XXX_' in direction:
                    patterns.append('live_three')
                elif '_XX_X_' in direction \
                        or 'X_XX' in direction:
                    patterns.append('jump_three')
                elif 'XXX__' in direction \
                        or '__XXX' in direction:
                    patterns.append('dead_three')
                elif '_XX_' in direction:
                    patterns.append('live_two')
                elif '__XX' in direction \
                        or 'XX__' in direction:
                    patterns.append('dead_two')
                elif '___X___' in direction:
                    patterns.append('single')
    return patterns


def local_patterns_detect(board, r, c, side):
    def convert(p, side):
        if (side == "a" and p == "◼︎") or (side == "b" and p == "☐"):
            return 'X'
        elif p == "":
            return '_'
        else:
            return 'O'

    def local_line(dx, dy):
        start_r, start_c = r, c
        move_index = 0
        board_size = len(board)
        while (0 <= start_r - dx < board_size
               and 0 <= start_c - dy < board_size):
            start_r -= dx
            start_c -= dy
            move_index += 1
        line = ''.join(convert(p, side) for p in
                       get_line(board, start_r, start_c, dx, dy))
        return line, move_index

    def contains_move(line, move_index, pattern):
        start = line.find(pattern)
        while start != -1:
            if start <= move_index < start + len(pattern):
                return True
            start = line.find(pattern, start + 1)
        return False

    patterns = []
    # downwards
    down = local_line(0, 1)
    # rightwards
    right = local_line(1, 0)
    # right_down
    right_down = local_line(1, 1)
    # right_up
    right_up = local_line(-1, 1)

    directions = [down, right, right_down, right_up]
    for direction, move_index in directions:
        if contains_move(direction, move_index, 'XXXXX'):
            patterns.append('five')
        elif contains_move(direction, move_index, '_XXXX_'):
            patterns.append('live_four')
        elif contains_move(direction, move_index, '_XXX_X') \
                or contains_move(direction, move_index, '_XX_XX') \
                or contains_move(direction, move_index, '_X_XXX'):
            patterns.append('jump_four')
        elif contains_move(direction, move_index, '_XXXX') \
                or contains_move(direction, move_index, 'XXXX_'):
            patterns.append('dead_four')
        elif contains_move(direction, move_index, '_XXX_'):
            patterns.append('live_three')
        elif contains_move(direction, move_index, '_XX_X_') \
                or contains_move(direction, move_index, 'X_XX'):
            patterns.append('jump_three')
        elif contains_move(direction, move_index, 'XXX__') \
                or contains_move(direction, move_index, '__XXX'):
            patterns.append('dead_three')
        elif contains_move(direction, move_index, '_XX_'):
            patterns.append('live_two')
        elif contains_move(direction, move_index, '__XX') \
                or contains_move(direction, move_index, 'XX__'):
            patterns.append('dead_two')
        elif contains_move(direction, move_index, '___X___'):
            patterns.append('single')
    return patterns


def score_cnt(patterns):
    inner_score = 0
    for pattern_ in patterns:
        inner_score += score[pattern_]
    return inner_score


def score_evaluate(board, side):
    myscore = 0
    myscore += score_cnt(global_patterns_detect(board, side))
    return myscore


def evaluate(board, side):
    my_score = score_evaluate(board, side)
    enemy_score = score_evaluate(board, opposite(side))
    return my_score - 1.2 * enemy_score


def minimax(board, ai_side, is_maximized, alpha, beta, depth, turns):
    key = (board_key(board), ai_side, depth, is_maximized, turns_range(turns))
    if key in TT:
        return TT[key]
    if win(board) or depth == 0:
        score = evaluate(board, ai_side)
        TT[key] = score
        return score
    possible_moves = get_candidate_move(board, radius_adjust(turns))
    if not possible_moves:
        score = evaluate(board, ai_side)
        TT[key] = score
        return score
    # scored_moves = []

    # for move in possible_moves:
    #     make_move(board, move, side)
    #     score = evaluate(board, side)
    #     undo_move(board, move)
    #     scored_moves.append(move)

    # scored_moves = sorted(possible_moves, key=lambda x: evaluate_move(x, board, side, 1)[1])
    scored_moves = possible_moves

    # ai's decision (max layer)
    if is_maximized:
        best_score = float('-inf')
        for move in scored_moves:
            make_move(board, move, ai_side)
            score = minimax(board, ai_side, False, alpha, beta, depth - 1, turns)
            undo_move(board, move)
            best_score = max(best_score, score)
            alpha = max(score, alpha)
            if alpha >= beta:
                return best_score
        TT[key] = best_score
        return best_score
    # player's decision (min layer)
    if not is_maximized:
        best_score = float('inf')
        for move in scored_moves:
            make_move(board, move, opposite(ai_side))
            score = minimax(board, ai_side, True, alpha, beta, depth - 1, turns)
            undo_move(board, move)
            best_score = min(best_score, score)
            beta = min(score, beta)
            if alpha >= beta:
                return best_score
        TT[key] = best_score
        return best_score


def evaluate_move(move, board, side, ai_side, depth, turns):
    # board_copy = copy.deepcopy(board)
    make_move(board, move, side)
    next_maximizing = (side != ai_side)
    score = minimax(board, ai_side, next_maximizing, float('-inf'), float('inf'), depth - 1, turns)
    undo_move(board, move)
    return [move, score]


def get_candidate_move(board, radius):
    size = len(board)
    occupied = []
    for r in range(size):
        for c in range(size):
            if board[r][c] != "":
                occupied.append((c, r))
    candidates = set()
    if not occupied:
        candidates.add((random.randint(5, 9), random.randint(5, 9)))
        return list(candidates)
    for (c, r) in occupied:
        for dr in range(-radius, radius + 1):
            for dc in range(-radius, radius + 1):
                nc, nr = c + dc, r + dr
                if 0 <= nc < size and 0 <= nr < size:
                    if board[nr][nc] == "":
                        candidates.add((nc, nr))
    return list(candidates)


def radius_adjust(turns):
    if turns_range(turns) == 'start':
        return 2
    elif turns_range(turns) == 'middle':
        return 3
    elif turns_range(turns) == 'end':
        return 5


def get_forced_moves(board, side, turns):
    for move in get_candidate_move(board, 2):
        make_move(board, move, side)
        if 'five' in local_patterns_detect(board, move[1], move[0], side):
            undo_move(board, move)
            return move
        undo_move(board, move)
    for move in get_candidate_move(board, 2):
        make_move(board, move, opposite(side))
        if 'five' in local_patterns_detect(board, move[1], move[0], opposite(side)):
            undo_move(board, move)
            return move
        undo_move(board, move)
    for move in get_candidate_move(board, 2):
        make_move(board, move, side)
        if 'live_four' in local_patterns_detect(board, move[1], move[0], side):
            undo_move(board, move)
            return move
        undo_move(board, move)
    for move in get_candidate_move(board, 2):
        make_move(board, move, opposite(side))
        if ('live_four' in local_patterns_detect(board, move[1], move[0], opposite(side))
                or 'live_three' in local_patterns_detect(board, move[1], move[0], opposite(side))
                or 'dead_four' in local_patterns_detect(board, move[1], move[0], opposite(side))):
            undo_move(board, move)
            return move
        undo_move(board, move)


def get_best_move(board, side, ai_side, depth, turns):
    global TT
    if len(TT) > 200000:
        TT = {}
    best_score = float('-inf')
    best_move = None
    # with ProcessPoolExecutor() as executor:
    #     for val in executor.map(evaluate_move, get_possible_moves(board),
    #                             repeat(board), repeat(side), repeat(depth)):
    #         if val[1] > best_score:
    #             best_score = val[1]
    #             best_move = val[0]
    candidates = get_candidate_move(board, radius_adjust(turns))
    if not candidates:
        candidates = get_possible_moves(board)
    if not candidates:
        return None
    forced_move = get_forced_moves(board, side, turns)
    if forced_move:
        best_move = forced_move
        best_move = f'{chr(best_move[0] + 97)}{best_move[1] + 1}'
        return best_move
    for move in candidates:
        move_, score = evaluate_move(move, board, side, ai_side, depth, turns)
        if score > best_score:
            best_score = score
            best_move = move_
    if best_move is None:
        return None
    best_move = f'{chr(best_move[0] + 97)}{best_move[1] + 1}'
    return best_move  # string
