from board import display_board
from ai import *
import os
import sys
import time
enable_ai = False
side = ""
ai_side = ""
depth = 0
turns = 0

if sys.platform == 'darwin':
    command = "clear"  # only for macOS; windows: os.system("cls")
else:
    command = "cls"


def turns_range(turns):
    if turns < 10:
        return "start"
    elif 10 <= turns < 30:
        return "middle"
    elif turns >= 30:
        return "end"


def menu():
    global enable_ai, ai_side, depth, side
    while True:
        choice = input("--Gomoku--\na.Player\nb.AI\nEnter your choice(a or b):")
        if choice.lower() == "a":
            enable_ai = False
            side = ""
            return
        elif choice.lower() == "b":
            while True:
                enable_ai = True
                while True:
                    depth = input("Choose the depth of AI (1~3):")
                    if not depth.isdigit():
                        print("Invalid input. Enter again:")
                    else:
                        depth = int(depth)
                        break
                if depth > 3:
                    confirm = input("⚠️  DO NOT ADJUST DEPTH GREATER THAN 3 UNLESS YOU KNOW WHAT YOU ARE DOING\n"
                                    "Confirm: y/n\n")
                    if confirm.lower() == "y":
                        break
                elif depth < 1:
                    print("Please input a valid depth value")
                else:
                    break
            while True:
                side = input("a.Black or b.White:")
                if side.lower() in "ab" and len(side) == 1:
                    side = side.lower()
                    ai_side = opposite(side.lower())
                    break
                else:
                    print("Invalid input.Enter 'a' or 'b':")
            return
        else:
            print("Invalid choice.Enter again:")
            time.sleep(1)
            os.system(command)


# check if the coordinate is in board
def inboard(x, y, board_size):
    return 0 <= x < board_size and 0 <= y < board_size


def opposite(current_side):
    if current_side == 'a':
        return 'b'
    elif current_side == 'b':
        return 'a'


def get_line(board, row, col, dx, dy):
    line_box = []
    board_size = len(board)
    for i in range(board_size):
        x = row + i * dx
        y = col + i * dy
        if inboard(x, y, board_size):
            line_box.append(board[x][y])
        else:
            break
    return line_box


def get_possible_moves(state):
    possible_moves = []
    for row_num in range(len(state)):
        row = state[row_num]
        for col in range(len(row)):
            box = row[col]
            if box == "":
                possible_moves.append([col, row_num])
    if not possible_moves:
        return None
    return possible_moves  # list


def win(board):
    is_win = False
    for row_num in range(len(board)):
        row = board[row_num]
        for col_num in range(len(row)):
            box = row[col_num]
            if box == "":
                continue
            piece_in_line = 0
            # downwards
            for piece in get_line(board, row_num, col_num, 0, 1):
                if piece == box and piece != "":
                    piece_in_line += 1
                if piece == "" or piece != box:
                    piece_in_line = 0
                if piece_in_line == 5:
                    is_win = True
            piece_in_line = 0
            # rightwards
            for piece in get_line(board, row_num, col_num, 1, 0):
                if piece == box and piece != "":
                    piece_in_line += 1
                if piece == "" or piece != box:
                    piece_in_line = 0
                if piece_in_line == 5:
                    is_win = True
            piece_in_line = 0
            # right-down
            for piece in get_line(board, row_num, col_num, 1, 1):
                if piece == box and piece != "":
                    piece_in_line += 1
                if piece == "" or piece != box:
                    piece_in_line = 0
                if piece_in_line == 5:
                    is_win = True
            # right-up
            piece_in_line = 0
            for piece in get_line(board, row_num, col_num, -1, 1):
                if piece == box and piece != "":
                    piece_in_line += 1
                if piece == "" or piece != box:
                    piece_in_line = 0
                if piece_in_line == 5:
                    is_win = True
    return is_win


def play():
    global turns

    def get_move(enable_ai, turns, side, state):
        if not enable_ai:
            fn_move = input(f"{"Black" if turns % 2 == 0 else "White"} turn.\nEnter coordinate of your move:")
        else:
            if turns % 2 == 0:
                if side == "a":
                    fn_move = input("Black turn.\nEnter coordinate of your move:")
                else:
                    # fn_move = random_move(board)
                    fn_move = get_best_move(state, ai_side, ai_side, depth, turns)
            else:
                if side == "b":
                    fn_move = input("White turn.\nEnter coordinate of your move:")
                else:
                    # fn_move = random_move(board)
                    fn_move = get_best_move(state, ai_side, ai_side, depth, turns)
        if type(fn_move) is list:  # move from AI
            raise Exception("Type of move is list.")
        return fn_move

    menu()
    os.system(command)
    print("---GOMOKU---")
    # initial board
    board = [
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    ]
    print(display_board(board))
    turns = 0
    opponent_move = "None"
    while True:
        is_valid = False
        while not is_valid:
            is_valid = True
            move = get_move(enable_ai, turns, side, board)
            if move is None and enable_ai:
                print("AI has no move. Game over.")
                return
            if (len(move) < 2
                    or move[0].lower() not in "abcdefghijklmno"
                    or not move[1:].isascii()
                    or not move[1:].isdigit()):
                print("Invalid input.Please enter again:")
                is_valid = False
                continue
            move_col = ord(move[0].lower()) - 97
            move_row = int(move[1:])
            if not inboard(move_col, move_row - 1, len(board)):
                print("Out of the board.Please enter another coordinate:")
                is_valid = False
                continue
            if board[move_row - 1][move_col] != "":
                print("Occupied place.Please enter another coordinate:")
                is_valid = False
                continue
        if turns % 2 == 0:
            board[move_row - 1][move_col] = "◼︎"
        else:
            board[move_row - 1][move_col] = "☐"
        if (turns % 2 == 0 and ai_side == "a") or (turns % 2 == 1 and ai_side == "b") or (not enable_ai):
            opponent_move = move
        os.system(command)
        print(f'--Gomoku--\n{display_board(board)}')
        print(f"Opponent's move:{opponent_move}")
        if win(board):
            print("-" * 40)
            print(f"{'Black' if turns % 2 == 0 else 'White'} win!")
            print("-" * 40)
            break
        if turns == len(board) ** 2 - 1:
            print("-" * 40)
            print("Draw!")
            print("-" * 40)
            break
        turns += 1


if __name__ == "__main__":
    try:
        play()
    except KeyboardInterrupt:
        print("\nProgram End")
        sys.exit(0)
