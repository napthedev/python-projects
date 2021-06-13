import pygame
import math

board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]

pygame.init()

window = pygame.display.set_mode((len(board[0]) * 60, len(board) * 60 + 60))
pygame.display.set_caption("Connect 4")

clock = pygame.time.Clock()
font = pygame.font.Font("freesansbold.ttf", 30)


def flip_board(board):
    new_board = []
    for i in range(len(board) - 1, -1, -1):
        new_board.append(board[i])
    return new_board


def draw_pointer(x, color):
    pygame.draw.circle(window, color, (x, 30), 28)


def draw(board, current_col):
    global mouseCol, winner
    pygame.draw.rect(window, (0, 0, 255),
                     (0, 60, len(board[0]) * 60, len(board) * 60))
    if current_col and winner is None:
        pygame.draw.rect(window, (70, 70, 255),
                         (mouseCol * 60, 60, 60, len(board) * 60))
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:
                pygame.draw.circle(window, (0, 0, 0),
                                   (col * 60 + 30, row * 60 + 90), 28)
            elif board[row][col] == 1:
                pygame.draw.circle(window, (255, 0, 0),
                                   (col * 60 + 30, row * 60 + 90), 28)
            elif board[row][col] == 2:
                pygame.draw.circle(window, (255, 255, 0),
                                   (col * 60 + 30, row * 60 + 90), 28)


def available_col(board, col):
    return board[5][col] == 0


def valid_locations(board):
    valid = []
    for col in range(len(board[0])):
        if available_col(board, col):
            valid.append(col)
    return valid


def drop(board, col, piece):
    for row in range(len(board)):
        if board[row][col] == 0:
            board[row][col] = piece
            break


def checkwin(board):
    # Horizontal
    for row in range(len(board)):
        for col in range(len(board[row]) - 3):
            if board[row][col] == board[row][
                    col + 1] and board[row][col] == board[row][
                        col + 2] and board[row][col] == board[row][
                            col + 3] and board[row][col] != 0:
                return board[row][col]

    # Vertical
    for row in range(len(board) - 3):
        for col in range(len(board[row])):
            if board[row][col] == board[row + 1][col] and board[row][
                    col] == board[row + 2][col] and board[row][col] == board[
                        row + 3][col] and board[row][col] != 0:
                return board[row][col]

    # Forward slash
    for row in range(len(board) - 3):
        for col in range(len(board[row]) - 3):
            if board[row][col] == board[row + 1][
                    col + 1] and board[row][col] == board[row + 2][
                        col + 2] and board[row][col] == board[row + 3][
                            col + 3] and board[row][col] != 0:
                return board[row][col]

    # Back slash
    for row in range(3, len(board)):
        for col in range(len(board[row]) - 3):
            if board[row][col] == board[row - 1][
                    col + 1] and board[row][col] == board[row - 2][
                        col + 2] and board[row][col] == board[row - 3][
                            col + 3] and board[row][col] != 0:
                return board[row][col]

    # Tie
    tie_count = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] != 0:
                tie_count += 1
    if tie_count >= len(board) * len(board[0]):
        return "tie"

    return None


def line_state(line, piece, op):
    score = 0
    if line.count(piece) == 3 and line.count(0) == 1:
        score += 500
    if line.count(piece) == 2 and line.count(0) == 2:
        score += 50

    if line.count(op) == 3 and line.count(0) == 1:
        score -= 300
    if line.count(op) == 2 and line.count(0) == 2:
        score -= 20

    return score


def checkscore(board, piece, op):
    score = 0

    # Horizontal
    for row in range(len(board)):
        for col in range(len(board[row]) - 3):
            row_list = board[row][col:col + 4]
            score += line_state(row_list, piece, op)

    # Vertical
    for row in range(len(board) - 3):
        for col in range(len(board[row])):
            score += line_state(row_list, piece, op)

    # Back slash
    for row in range(len(board) - 3):
        for col in range(len(board[row]) - 3):
            back_slash_list = [
                board[row][col], board[row + 1][col + 1],
                board[row + 2][col + 2], board[row + 3][col + 3]
            ]
            score += line_state(back_slash_list, piece, op)

    # Forward slash
    for row in range(3, len(board)):
        for col in range(len(board[row]) - 3):
            forward_slash_list = [
                board[row][col], board[row - 1][col + 1],
                board[row - 2][col + 2], board[row - 3][col + 3]
            ]
            score += line_state(forward_slash_list, piece, op)

    return score


def ai_move(board, piece):
    best_score = -math.inf
    best_col = len(board[0]) // 2
    valid = valid_locations(board)
    pygame.draw.rect(window, (0, 0, 0), (0, 0, 420, 60))
    draw(flip_board(board), False)
    pygame.display.update()
    for col in valid:
        drop(board, col, piece)
        score = minimax(board, 3, False)
        for row in range(len(board) - 1, -1, -1):
            if board[row][col] != 0:
                board[row][col] = 0
                break
        if col == len(board[0]) // 2:
            score += 250
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def minimax(board, depth, maximizing):
    score = checkwin(board)
    if score == 1:
        return -10000000 - depth
    elif score == 2:
        return 10000000000 + depth
    elif score == "tie":
        return 0

    if depth <= 0:
        return checkscore(board, 2, 1) + depth

    if maximizing:
        best_score = -math.inf
        valid = valid_locations(board)
        for col in valid:
            drop(board, col, 2)
            score = minimax(board, depth - 1, False)
            for row in range(len(board) - 1, -1, -1):
                if board[row][col] != 0:
                    board[row][col] = 0
                    break
            if score > best_score:
                best_score = score

        return best_score

    else:
        best_score = math.inf
        valid = valid_locations(board)
        for col in valid:
            drop(board, col, 1)
            score = minimax(board, depth - 1, True)
            for row in range(len(board) - 1, -1, -1):
                if board[row][col] != 0:
                    board[row][col] = 0
                    break
            if score < best_score:
                best_score = score

        return best_score


running = True
mouseX = 210
turn = 1
mouseCol = 3
winner = None
while running:
    window.fill((0, 0, 0))

    if turn % 2 == 0 and winner is None:
        mouseCol = ai_move(board, 2)
        if available_col(board, mouseCol):
            drop(board, mouseCol, 2)
            turn += 1
            winner = checkwin(board)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mouseCol = event.pos[0] // 60
            mouseX = event.pos[0]
            if mouseX < 30:
                mouseX = 30
            elif mouseX > len(board[0]) * 60 - 30:
                mouseX = len(board[0]) * 60 - 30
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseCol = event.pos[0] // 60
            if available_col(board, mouseCol) and winner is None:
                if turn % 2 == 1:
                    drop(board, mouseCol, 1)
                    turn += 1
                    winner = checkwin(board)

    draw(flip_board(board), True)

    if winner is None:
        draw_pointer(mouseX, (255, 0, 0))

    if winner is not None:
        if winner == 1:
            win_text = font.render(f"YOU WINS", True, (255, 0, 0))
        elif winner == 2:
            win_text = font.render(f"COMPUTER WINS", True, (255, 255, 0))
        elif winner == "tie":
            win_text = font.render(f"TIE", True, (255, 255, 255))
        win_text_rect = win_text.get_rect(center=(210, 30))
        window.blit(win_text, win_text_rect)

    clock.tick(24)
    pygame.display.update()
