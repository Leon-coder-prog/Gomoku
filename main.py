from board import display_board
from ai import *
import os
import time
enable_ai = False
depth = 0


def menu():
    global enable_ai, depth
    while True:
        choice = input("--Gomoku--\na.Player\nb.AI\nEnter your choice(a or b):")
        if choice.lower() == "a":
            enable_ai = False
            return
        elif choice.lower() == "b":
            enable_ai = True
            depth = int(input("Choose the depth of AI (1~3):"))
            return
        else:
            print("Invalid choice.Enter again:")
            time.sleep(1)
            os.system("clear")


# check if the coordinate is in board
def inboard(x, y, board_size):
    return 0 <= x <= board_size and 0 <= y <= board_size


def opposite(side):
    if side == 'a':
        return 'b'
    elif side == 'b':
        return 'a'


def get_line(board, row, col, dx, dy):
    line_box = []
    board_size = len(board) - 1
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
            piece_in_line = 0
            # downwards
            for piece in get_line(board, row_num, col_num, 0, 1):
                if piece == box and piece != "":
                    piece_in_line += 1
                if piece == "":
                    piece_in_line = 0
                if piece_in_line == 5:
                    is_win = True
            piece_in_line = 0
            # rightwards
            for piece in get_line(board, row_num, col_num, 1, 0):
                if piece == box and piece != "":
                    piece_in_line += 1
                if piece == "":
                    piece_in_line = 0
                if piece_in_line == 5:
                    is_win = True
            piece_in_line = 0
            # right-down
            for piece in get_line(board, row_num, col_num, 1, 1):
                if piece == box and piece != "":
                    piece_in_line += 1
                if piece == "":
                    piece_in_line = 0
                if piece_in_line == 5:
                    is_win = True
            # right-up
            piece_in_line = 0
            for piece in get_line(board, row_num, col_num, -1, 1):
                if piece == box and piece != "":
                    piece_in_line += 1
                if piece == "":
                    piece_in_line = 0
                if piece_in_line == 5:
                    is_win = True
    return is_win


def play():
    def get_move(enable_ai, turns, side, state):
        if not enable_ai:
            fn_move = input(f"{"Black" if turns % 2 == 0 else "White"} turn.\nEnter coordinate of your move:")
        else:
            if turns % 2 == 0:
                if side == "a":
                    fn_move = input("Black turn.\nEnter coordinate of your move:")
                else:
                    # fn_move = random_move(board)
                    fn_move = get_best_move(state, side, depth)
            else:
                if side == "b":
                    fn_move = input("White turn.\nEnter coordinate of your move:")
                else:
                    # fn_move = random_move(board)
                    fn_move = get_best_move(state, side, depth)
        if type(fn_move) is list:  # move from AI
            raise Exception("Type of move is list.")
        return fn_move

    menu()
    if enable_ai:
        while True:
            side = input("a.Black or b.White:")
            if side.lower() in "ab":
                break
            else:
                print("Invalid input.Enter 'a' or 'b':")
    else:
        side = None
    os.system("clear")
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
    while True:
        is_valid = False
        while not is_valid:
            is_valid = True
            move = get_move(enable_ai, turns, side, board)
            if move is None:
                print("AI has no move. Game over.")
                break
            if move[0].isdigit() or not move[1].isdigit():
                print("Invalid input.Please enter again:")
                is_valid = False
                continue
            move_col = ord(move[0]) - 97
            try:
                move_row = int(move[1:])
            except ValueError:
                print("Invalid input.Please enter again:")
                is_valid = False
                continue
            if move_col > 14 or move_row > 14:
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
        os.system("clear")  # only for macOS; windows: os.system("cls")
        print(display_board(board))
        if win(board):
            print(f"{'Black' if turns % 2 == 0 else 'White'} win!")
            break
        turns += 1


if __name__ == "__main__":
    play()
