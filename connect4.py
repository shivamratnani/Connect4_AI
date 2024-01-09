import numpy as np
import pygame
import sys
import math
import random
from threading import Timer

# Global Constants
ROWS, COLS = 6, 7
PLAYER_TURN, AI_TURN = 0, 1
PLAYER_PIECE, AI_PIECE = 1, 2
BLUE, BLACK, RED, YELLOW = (0, 0, 255), (0, 0, 0), (255, 0, 0), (255, 255, 0)

# Create an empty game board.
def create_board():
    return np.zeros((ROWS, COLS))

# Place a game piece on the board.
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Check if a column is a valid move.
def is_valid_location(board, col):
    return board[0][col] == 0

# Get the next available row in a column.
def get_next_open_row(board, col):
    for r in reversed(range(ROWS)):
        if board[r][col] == 0:
            return r

# Check if a player has won the game.
def winning_move(board, piece):
    for c in range(COLS-3):
        for r in range(ROWS):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    for c in range(3, COLS):
        for r in range(3, ROWS):
            if all(board[r-i][c-i] == piece for i in range(4)):
                return True
    return False

# Draw the game board on the screen.
def draw_board(board, screen, SQUARESIZE, circle_radius):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            color = BLACK if board[r][c] == 0 else RED if board[r][c] == PLAYER_PIECE else YELLOW
            pygame.draw.circle(screen, color, (int(c * SQUARESIZE + SQUARESIZE/2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
    pygame.display.update()

# Evaluate the score of a window of 4 game pieces.
def evaluate_window(window, piece):
    score = 0
    opponent_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2
    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4
    return score

# Evaluate the score of the current game position.
def score_position(board, piece):
    score = 0
    center_array = [int(i) for i in list(board[:, COLS//2])]
    score += center_array.count(piece) * 6
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLS - 3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)
    for c in range(COLS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROWS-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)
    for r in range(3, ROWS):
        for c in range(COLS-3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)
        for c in range(3, COLS):
            window = [board[r-i][c-i] for i in range(4)]
            score += evaluate_window(window, piece)
    return score

# Check if the current game position is a terminal node.
def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

# Implement the minimax algorithm to determine the best move.
def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return None, 10000000
            elif winning_move(board, PLAYER_PIECE):
                return None, -10000000
            else:
                return None, 0
        else:
            return None, score_position(board, AI_PIECE)

    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(value, alpha)
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(value, beta)
            if alpha >= beta:
                break
        return column, value

# Get a list of valid column locations to make a move.
def get_valid_locations(board):
    return [col for col in range(COLS) if is_valid_location(board, col)]

# End the game.
def end_game():
    global game_over
    game_over = True
    print("Game over:", game_over)

# Initialize and Run the Game
board = create_board()
game_over = False
not_over = True
turn = random.randint(PLAYER_TURN, AI_TURN)

pygame.init()
SQUARESIZE = 100
width, height = COLS * SQUARESIZE, (ROWS + 1) * SQUARESIZE
circle_radius = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode((width, height))
my_font = pygame.font.SysFont("monospace", 75)
draw_board(board, screen, SQUARESIZE, circle_radius)

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION and not_over:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            xpos = event.pos[0]
            if turn == PLAYER_TURN:
                pygame.draw.circle(screen, RED, (xpos, int(SQUARESIZE/2)), circle_radius)

        if event.type == pygame.MOUSEBUTTONDOWN and not_over:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            if turn == PLAYER_TURN:
                xpos = event.pos[0]
                col = int(xpos // SQUARESIZE)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)
                    if winning_move(board, PLAYER_PIECE):
                        label = my_font.render("PLAYER 1 WINS!", 1, RED)
                        screen.blit(label, (40, 10))
                        not_over = False
                        Timer(3.0, end_game).start()
                    turn = AI_TURN  # Change turn to AI
            draw_board(board, screen, SQUARESIZE, circle_radius)

    if turn == AI_TURN and not game_over and not_over:
        col, _ = minimax(board, 5, -math.inf, math.inf, True)
        if is_valid_location(board, col):
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            if winning_move(board, AI_PIECE):
                label = my_font.render("PLAYER 2 WINS!", 1, YELLOW)
                screen.blit(label, (40, 10))
                not_over = False
                Timer(3.0, end_game).start()
            turn = PLAYER_TURN  # Change turn back to player
        draw_board(board, screen, SQUARESIZE, circle_radius)

    pygame.display.update()
