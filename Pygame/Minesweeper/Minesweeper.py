import pygame
import random
from tkinter import *
from tkinter import messagebox


pygame.init()

window = pygame.display.set_mode((288, 288))
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 20)


real_board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]


display_board = [
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None]
]


number_bombs = 10
for i in range(number_bombs):
    row = random.randint(0, 8)
    col = random.randint(0, 8)
    while real_board[row][col] == "bomb":
        row = random.randint(0, 8)
        col = random.randint(0, 8)
    real_board[row][col] = "bomb"


for row in range(9):
    for col in range(9):
        if real_board[row][col] != "bomb":
            left = True
            right = True
            top = True
            bottom = True
            count = 0

            if row == 0:
                top = False
            if row == 8:
                bottom = False
            if col == 0:
                left = False
            if col == 8:
                right = False

            if top:
                if real_board[row - 1][col] == "bomb":
                    count += 1

            if left:
                if real_board[row][col - 1] == "bomb":
                    count += 1

            if right:
                if real_board[row][col + 1] == "bomb":
                    count += 1

            if bottom:
                if real_board[row + 1][col] == "bomb":
                    count += 1

            if top and left:
                if real_board[row - 1][col - 1] == "bomb":
                    count += 1

            if top and right:
                if real_board[row - 1][col + 1] == "bomb":
                    count += 1

            if bottom and left:
                if real_board[row + 1][col - 1] == "bomb":
                    count += 1

            if bottom and right:
                if real_board[row + 1][col + 1] == "bomb":
                    count += 1

            real_board[row][col] = count


def empty_clicked(row, col):
    global real_board, display_board
    left = True
    right = True
    top = True
    bottom = True

    if row == 0:
        top = False
    if row == 8:
        bottom = False
    if col == 0:
        left = False
    if col == 8:
        right = False

    if top:
        if real_board[row - 1][col] != "bomb":
            if real_board[row - 1][col] == 0 and display_board[row - 1][col] != 0:
                display_board[row - 1][col] = 0
                empty_clicked(row - 1, col)
            else:
                display_board[row - 1][col] = real_board[row - 1][col]

    if left:
        if real_board[row][col - 1] != "bomb":
            if real_board[row][col - 1] == 0 and display_board[row][col - 1] != 0:
                display_board[row][col - 1] = 0
                empty_clicked(row, col - 1)
            else:
                display_board[row][col - 1] = real_board[row][col - 1]

    if right:
        if real_board[row][col + 1] != "bomb":
            if real_board[row][col + 1] == 0 and display_board[row][col + 1] != 0:
                display_board[row][col + 1] = 0
                empty_clicked(row, col + 1)
            else:
                display_board[row][col + 1] = real_board[row][col + 1]

    if bottom:
        if real_board[row + 1][col] != "bomb":
            if real_board[row + 1][col] == 0 and display_board[row + 1][col] != 0:
                display_board[row + 1][col] = 0
                empty_clicked(row + 1, col)
            else:
                display_board[row + 1][col] = real_board[row + 1][col]

    if top and left:
        if real_board[row - 1][col - 1] != "bomb":
            if real_board[row - 1][col - 1] == 0 and display_board[row - 1][col - 1] != 0:
                display_board[row - 1][col - 1] = 0
                empty_clicked(row - 1, col - 1)
            else:
                display_board[row - 1][col - 1] = real_board[row - 1][col - 1]

    if top and right:
        if real_board[row - 1][col + 1] != "bomb":
            if real_board[row - 1][col + 1] == 0 and display_board[row - 1][col + 1] != 0:
                display_board[row - 1][col + 1] = 0
                empty_clicked(row - 1, col + 1)
            else:
                display_board[row - 1][col + 1] = real_board[row - 1][col + 1]

    if bottom and left:
        if real_board[row + 1][col - 1] != "bomb":
            if real_board[row + 1][col - 1] == 0 and display_board[row + 1][col - 1] != 0:
                display_board[row + 1][col - 1] = 0
                empty_clicked(row + 1, col - 1)
            else:
                display_board[row + 1][col - 1] = real_board[row + 1][col - 1]

    if bottom and right:
        if real_board[row + 1][col + 1] != "bomb":
            if real_board[row + 1][col + 1] == 0 and display_board[row + 1][col + 1] != 0:
                display_board[row + 1][col + 1] = 0
                empty_clicked(row + 1, col + 1)
            else:
                display_board[row + 1][col + 1] = real_board[row + 1][col + 1]


def checkwin():
    global real_board, display_board, number_bombs, running, win
    count = 0
    for row in range(9):
        for col in range(9):
            if display_board[row][col] is not None:
                count += 1
    if count >= 81 - number_bombs:
        draw()
        running = False
        win = True


def draw():
    for row in range(9):
        for col in range(9):
            if display_board[row][col] is None:
                pygame.draw.polygon(window, (255, 255, 255), [(row * 32, col * 32 + 32), (row * 32, col * 32), (row * 32 + 32, col * 32)])
                pygame.draw.polygon(window, (128, 128, 128), [(row * 32, col * 32 + 32), (row * 32 + 32, col * 32 + 32), (row * 32 + 32, col * 32)])
                pygame.draw.rect(window, (198, 198, 198), (row * 32 + 4, col * 32 + 4, 24, 24))
            else:
                pygame.draw.rect(window, (128, 128, 128), (row * 32, col * 32, 32, 32), 1)

            if display_board[row][col] == "bomb":
                pygame.draw.circle(window, (0, 0, 0), (row * 32 + 16, col * 32 + 16), 8)
                pygame.draw.line(window, (0, 0, 0), (row * 32 + 15, col * 32 + 5), (row * 32 + 15, col * 32 + 26), 2)
                pygame.draw.line(window, (0, 0, 0), (row * 32 + 5, col * 32 + 15), (row * 32 + 26, col * 32 + 15), 2)
                pygame.draw.line(window, (0, 0, 0), (row * 32 + 8, col * 32 + 8), (row * 32 + 22, col * 32 + 22), 2)
                pygame.draw.line(window, (0, 0, 0), (row * 32 + 8, col * 32 + 22), (row * 32 + 22, col * 32 + 8), 2)
                pygame.draw.rect(window, (255, 255, 255), (row * 32 + 12, col * 32 + 12, 4, 4))

            elif display_board[row][col] != 0 and display_board[row][col] is not None:
                font = pygame.font.Font('freesansbold.ttf', 20)
                if display_board[row][col] == 1:
                    text = font.render(str(display_board[row][col]), True, (0, 0, 255))
                elif display_board[row][col] == 2:
                    text = font.render(str(display_board[row][col]), True, (0, 255, 0))
                elif display_board[row][col] == 3:
                    text = font.render(str(display_board[row][col]), True, (255, 0, 0))
                elif display_board[row][col] == 4:
                    text = font.render(str(display_board[row][col]), True, (3, 2, 123))
                else:
                    text = font.render(str(display_board[row][col]), True, (127, 10, 10))
                window.blit(text, (row * 32 + 10, col * 32 + 8))


msg_box = True
running = True
while running:
    window.fill((255, 255, 255))
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            msg_box = False
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouseX = event.pos[0] // 32
            mouseY = event.pos[1] // 32
            if real_board[mouseX][mouseY] == "bomb":
                display_board = real_board.copy()
                draw()
                running = False
                win = False
            elif real_board[mouseX][mouseY] != 0:
                display_board[mouseX][mouseY] = real_board[mouseX][mouseY]
                checkwin()
            elif real_board[mouseX][mouseY] == 0:
                display_board[mouseX][mouseY] = 0
                empty_clicked(mouseX, mouseY)
                checkwin()

    clock.tick(24)
    pygame.display.update()


tk = Tk()
tk.withdraw()


if msg_box:
    if win:
        messagebox.showinfo("Congratulations!", "You win!")
    else:
        messagebox.showerror("Game over!", "You dug the bomb")
