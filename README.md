# Gomoku

This is a Python implementation of the classic Gomoku (Five in a Row) game. The program supports both human vs human and human vs AI modes with configurable AI search depth.

The AI part is complemented with Minimax algorithm coupled with alpha-beta pruning. Some other optimizations are also added.
## Features

- 15×15 board display
- Human vs Human gameplay
- Human vs AI gameplay
- Win condition detection

## Requirements

- Python 3.x

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   ```
2. Change into the project directory:
   ```bash
   cd your-repo-name
   ```
3. Run the game:
    ```bash
   python main.py
   ```
   If not working:
   ```bash
   python3 main.py
   ```
## Gameplay Instructions

When the program starts you will see a menu:
- Enter **a** or **b** to play **Human vs Human** or **Human vs AI**  

If you choose to play with AI, you will need to:
- Choose AI depth (1 to 3)  
   **_!Depth greater than 3 will have huge impact on CPU usage and running speed!_**
- Choose your side (Black or White)

During the game, enter moves in the format:
```commandline
a3
```
- The letter represents the column (a to o)
- The number represents the row (1 to 15)
## Win Rules
A player wins when they get 5 of their pieces in a row in any direction: horizontal, vertical, or diagonal.
## Project Structure
```code
.
├── main.py        # Main program
├── board.py       # Board display logic
├── ai.py          # AI logic
└── README.md      # This file
```
## License
This project is licensed under the MIT License. See the LICENSE file for details.