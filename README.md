# Connect Four with AI

## Overview

This Python program is an implementation of the classic game Connect Four, featuring a player-versus-AI mode. The game is built using the `pygame` library for graphical representation and `numpy` for handling the game board. The AI's decision-making is powered by the Minimax algorithm, a recursive algorithm for choosing the next move in games like chess and tic-tac-toe.

## Features

- **Graphical User Interface:** The game is visually represented, showing a grid where players and AI can drop their pieces.
- **Player vs. AI Gameplay:** One player competes against an AI opponent, which uses the Minimax algorithm to determine its moves.
- **Win Detection:** The game can detect and announce a win for either the player or the AI.
- **Dynamic Board Size:** The board dimensions can be easily adjusted through global constants.

## Requirements

- Python 3.x
- `pygame` library
- `numpy` library

## Installation

To run this game, you need to install Python and the required libraries. You can install the libraries using pip:

```bash
pip install pygame numpy
```

## Usage

To start the game, simply run the script:

```bash
python connect4.py
```

### Game Controls

- **Mouse Movement:** Move your mouse horizontally across the top of the game window to position your piece.
- **Mouse Click:** Click to drop your piece in the chosen column.
- **Close Window:** Click the close button on the window or press `ALT+F4` to exit the game.

## Game Rules

1. The game is played on a vertical board with 6 rows and 7 columns.
2. Each player has a set of colored pieces (Red for Player, Yellow for AI).
3. Players take turns dropping one of their pieces into the top of any column.
4. The piece will occupy the lowest available space within that column.
5. The objective is to be the first to form a horizontal, vertical, or diagonal line of four of one's own pieces.

## AI Algorithm

The AI uses the Minimax algorithm with a depth of 5 moves. It evaluates the board state to maximize its chance of winning while minimizing the player's chance of winning. The algorithm considers various factors such as the number of pieces in the center column and potential winning moves.

## Customization

You can customize various aspects of the game:

- **Board Size:** Change `ROWS` and `COLS` in the global constants.
- **AI Difficulty:** Adjust the depth parameter in the `minimax` function call. Higher values increase difficulty.

## Limitations

- The AI's performance is tied to the depth of the Minimax algorithm, which might slow down the game at higher depths.
- The graphical interface is basic and may not run as smoothly on all systems.

## Conclusion

This Python implementation of Connect Four offers an engaging way to play against a challenging AI opponent. It's a great project for those looking to understand game development and AI algorithms in Python.
