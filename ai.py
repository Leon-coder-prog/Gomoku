import random


def random_move(state):
    empty_box = []
    for row_num in range(len(state)):
        row = state[row_num]
        for col in range(len(row)):
            box = row[col]
            if box == "":
                empty_box.append(f"{chr(col+97)}{row_num}")
    if empty_box is None:
        return None
    move = random.choice(empty_box)
    return move
