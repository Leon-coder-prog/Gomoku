def display_board(board):
    display = ''
    row_num = 15
    for row in board[::-1]:  # Rows are read backwards since display is from top to bottom
        # If row_num >= 10, it will occupy 2 space. In this way, the grid of the board will not align.
        # Therefore, if row_num < 10, there is a more space following the row number.
        if row_num < 10:
            display += str(row_num) + '  '
        else:
            display += str(row_num) + ' '
        row_num -= 1
        for box in row:
            if box == "":
                display += "·"
            else:
                display += box[0]
            display += ' '
        display += '\n'
    display += '   a b c d e f g h i j k l m n o'
    return display

