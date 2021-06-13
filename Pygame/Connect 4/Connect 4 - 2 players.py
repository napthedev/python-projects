import pygame

board = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
]

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


def draw(board):
    global winner
    pygame.draw.rect(window, (0, 0, 255),
                     (0, 60, len(board[0]) * 60, len(board) * 60))
    if winner is None:
        pygame.draw.rect(window, (70, 70, 255),
                         (mouseCol * 60, 60, 60, len(board) * 60))
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 0:
                pygame.draw.circle(window, (0, 0, 0), (col * 60 + 30, row * 60 + 90), 28)
            elif board[row][col] == 1:
                pygame.draw.circle(window, (255, 0, 0), (col * 60 + 30, row * 60 + 90), 28)
            elif board[row][col] == 2:
                pygame.draw.circle(window, (255, 255, 0), (col * 60 + 30, row * 60 + 90), 28)


def available_col(board, col):
    return board[5][col] == 0


def drop(board, col, piece):
    for row in range(len(board)):
        if board[row][col] == 0:
            board[row][col] = piece
            break


def checkwin(board):
    # Horizontal
    for row in range(len(board)):
        for col in range(len(board[row]) - 3):
            if board[row][col] == board[row][col + 1] and board[row][col] == board[row][col + 2] and board[row][col] == board[row][col + 3] and board[row][col] != 0:
                return board[row][col]

    # Vertical
    for row in range(len(board) - 3):
        for col in range(len(board[row])):
            if board[row][col] == board[row + 1][col] and board[row][col] == board[row + 2][col] and board[row][col] == board[row + 3][col] and board[row][col] != 0:
                return board[row][col]

    # Forward slash
    for row in range(len(board) - 3):
        for col in range(len(board[row]) - 3):
            if board[row][col] == board[row + 1][col + 1] and board[row][col] == board[row + 2][col + 2] and board[row][col] == board[row + 3][col + 3] and board[row][col] != 0:
                return board[row][col]

    # Back slash
    for row in range(3, len(board)):
        for col in range(len(board[row]) - 3):
            if board[row][col] == board[row - 1][col + 1] and board[row][col] == board[row - 2][col + 2] and board[row][col] == board[row - 3][col + 3] and board[row][col] != 0:
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


running = True
mouseX = 210
turn = 1
color = (255, 0, 0)
mouseCol = 3
winner = None
while running:
    window.fill((0, 0, 0))
    draw(flip_board(board))

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
                else:
                    drop(board, mouseCol, 2)
                turn += 1
                winner = checkwin(board)

    if turn % 2 == 1:
        color = (255, 0, 0)
    else:
        color = (255, 255, 0)

    if winner is None:
        draw_pointer(mouseX, color)

    if winner is not None:
        if winner == 1:
            win_text = font.render(f"PLAYER RED WINS", True, (255, 0, 0))
        elif winner == 2:
            win_text = font.render(f"PLAYER YELLOW WINS", True, (255, 255, 0))
        elif winner == "tie":
            win_text = font.render(f"TIE", True, (255, 255, 255))
        win_text_rect = win_text.get_rect(center=(210, 30))
        window.blit(win_text, win_text_rect)

    pygame.display.update()
