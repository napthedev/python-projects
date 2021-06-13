import pygame

pygame.init()

window = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Tic Tac Toe")

clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 30)


def drawX(col, row):
    pygame.draw.line(window, (255, 0, 0), (col * 100 + 20, row * 100 + 20), (col * 100 + 80, row * 100 + 80), 10)
    pygame.draw.line(window, (255, 0, 0), (col * 100 + 80, row * 100 + 20), (col * 100 + 20, row * 100 + 80), 10)


def drawO(col, row):
    pygame.draw.circle(window, (0, 0, 255), (col * 100 + 50, row * 100 + 50), 35, 7)


win_type = None
win_row = 0
win_col = 0
winner = None


def checkwin():
    global win_row, win_col, win_type, winner, turn
    # Horizontal
    for row in range(3):
        if table[row][0] == table[row][1] and table[row][0] == table[row][2] and table[row][0] != 0:
            win_type = "horizontal"
            win_row = row
            return table[row][0]

    # Vertical
    for col in range(3):
        if table[0][col] == table[1][col] and table[0][col] == table[2][col] and table[0][col] != 0:
            win_type = "vertical"
            win_col = col
            return table[0][col]

    # Forward slash
    if table[0][0] == table[1][1] and table[0][0] == table[2][2] and table[0][0] != 0:
        win_type = "forward_slash"
        return table[0][0]

    # Back slash
    if table[0][2] == table[1][1] and table[0][2] == table[2][0] and table[0][2] != 0:
        win_type = "back_slash"
        return table[0][2]

    tie_count = 0
    for row in range(3):
        for col in range(3):
            if table[row][col] != 0:
                tie_count += 1
    if tie_count >= 9:
        return "tie"

    return None


def drawwinline(type, row, col):
    if type == "horizontal":
        pygame.draw.line(window, (0, 255, 0), (20, row * 100 + 50), (280, row * 100 + 50), 15)
    elif type == "vertical":
        pygame.draw.line(window, (0, 255, 0), (col * 100 + 50, 20), (col * 100 + 50, 280), 15)
    elif type == "forward_slash":
        pygame.draw.line(window, (0, 255, 0), (40, 40), (260, 260), 15)
    elif type == "back_slash":
        pygame.draw.line(window, (0, 255, 0), (260, 40), (40, 260), 15)


table = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
]

turn = 1
running = True
while running:
    window.fill((20, 189, 172, 255))
    pygame.draw.line(window, (13, 161, 146, 255), (100, 0), (100, 300), 5)
    pygame.draw.line(window, (13, 161, 146, 255), (200, 0), (200, 300), 5)
    pygame.draw.line(window, (13, 161, 146, 255), (0, 100), (300, 100), 5)
    pygame.draw.line(window, (13, 161, 146, 255), (0, 200), (300, 200), 5)

    for row in range(3):
        for col in range(3):
            if table[row][col] == 1:
                drawX(col, row)
            elif table[row][col] == 2:
                drawO(col, row)

    if winner == "tie":
        text = font.render("Tie", True, (255, 255, 255))
        window.blit(text, (130, 130))
    elif winner is not None:
        drawwinline(win_type, win_row, win_col)
        text = font.render(f"Player {winner} wins", True, (255, 255, 255))
        window.blit(text, (50, 130))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0] // 100
            mouseY = event.pos[1] // 100
            if table[mouseY][mouseX] == 0 and winner is None:
                if turn % 2 == 1:
                    table[mouseY][mouseX] = 1
                    turn += 1
                    winner = checkwin()
                else:
                    table[mouseY][mouseX] = 2
                    turn += 1
                    winner = checkwin()

    clock.tick(24)
    pygame.display.update()
